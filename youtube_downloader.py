import os
import re
import sys
import argparse
from pytube import YouTube, Playlist
from pytube.innertube import _default_clients
from pytube import cipher
from tqdm import tqdm

# ANSI escape codes for colors
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'

# Define RegexMatchError class
class RegexMatchError(Exception):
    def __init__(self, caller, pattern):
        super().__init__(f"Regex match error in {caller} with pattern: {pattern}")
        self.caller = caller
        self.pattern = pattern

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}#############################################################{Colors.RESET}
{Colors.CYAN}{Colors.BOLD}#                                                          #{Colors.RESET}
{Colors.CYAN}{Colors.BOLD}# {Colors.YELLOW}               {Colors.BOLD}	HACKWRLD{Colors.CYAN}{Colors.BOLD}                           #{Colors.RESET}
{Colors.CYAN}{Colors.BOLD}#                                                          #{Colors.RESET}
{Colors.CYAN}{Colors.BOLD}#############################################################{Colors.RESET}
"""
    print(banner)

# Apply the patch for client version issues
_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

# Patch for throttling function
def get_throttling_function_name(js: str) -> str:
    function_patterns = [
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )

cipher.get_throttling_function_name = get_throttling_function_name

# Function to get all video links from the playlist
def get_video_links(playlist_url):
    playlist = Playlist(playlist_url)
    video_links = [video.watch_url for video in playlist.videos]
    return video_links

# Function to download a video from a link with the highest resolution up to 1080p
def download_video(video_url, download_folder="./downloads", audio_only=False):
    try:
        yt = YouTube(video_url)
        print(f'{Colors.GREEN}Downloading: {Colors.RESET}{Colors.BLUE}{yt.title}{Colors.RESET}')
        
        # Define the output file path
        file_extension = 'mp3' if audio_only else 'mp4'
        output_file = os.path.join(download_folder, f"{yt.title}.{file_extension}")

        # Check if the file already exists
        if os.path.exists(output_file):
            print(f"{Colors.YELLOW}File already exists: {output_file}{Colors.RESET}")
            return
        
        if audio_only:
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.filter(res="1080p", progressive=True, file_extension='mp4').first()

            if not stream:
                available_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')
                for s in reversed(available_streams):
                    resolution = int(s.resolution[:-1])
                    if resolution <= 1080:
                        stream = s
                        break
        
        if stream:
            if stream.filesize is None:
                print(f"{Colors.RED}Stream filesize is not available for {yt.title}{Colors.RESET}")
                return

            with tqdm(total=stream.filesize, unit='B', unit_scale=True, unit_divisor=1024, 
                      bar_format="{l_bar}{bar} [elapsed: {elapsed} < {remaining}, {rate_fmt}]") as pbar:
                try:
                    stream.download(output_path=download_folder)
                    pbar.update(stream.filesize)  # Update progress to complete after download
                except KeyboardInterrupt:
                    print(f"\n{Colors.RED}Download interrupted: {yt.title}{Colors.RESET}")
                    return
            
            print(f'{Colors.GREEN}Video downloaded: {Colors.RESET}{Colors.BLUE}{yt.title} in {Colors.RED}{stream.resolution}{Colors.RESET}')
        else:
            print(f'{Colors.YELLOW}No suitable resolution available for {yt.title}{Colors.RESET}')
    
    except KeyboardInterrupt:
        global args  # Add this line to make 'args' accessible
        if args.url.startswith('playlist'):
            choice = input(f"\n{Colors.YELLOW}Download interrupted. Do you want to continue to the next video in the playlist? (y/n): {Colors.RESET}")
            if choice.lower() == 'y':
                return  # Continue to the next video
            else:
                print(f"{Colors.RED}Exiting the program.{Colors.RESET}")
                sys.exit(0)
        else:
            choice = input(f"\n{Colors.YELLOW}Download interrupted. Do you really want to exit? (y/n): {Colors.RESET}")
            if choice.lower() == 'y':
                print(f"{Colors.RED}Exiting the program.{Colors.RESET}")
                sys.exit(0)
            else:
                return  # Continue with the current video

# Function to download all videos from the playlist links
def download_videos_from_playlist(playlist_url, audio_only=False):
    video_links = get_video_links(playlist_url)
    
    # Create a download folder
    download_folder = './downloads'
    os.makedirs(download_folder, exist_ok=True)
    
    # Download each video using its link
    for link in video_links:
        download_video(link, download_folder, audio_only)

def get_links_from_file(file_path):
    with open(file_path, 'r') as file:
        links = file.read().splitlines()
    return links

def download_videos_from_file(file_path, audio_only=False):
    video_links = get_links_from_file(file_path)
    download_folder = './downloads'
    os.makedirs(download_folder, exist_ok=True)
    
    for link in video_links:
        if 'playlist' in link:
            download_videos_from_playlist(link, audio_only)
        else:
            download_video(link, download_folder, audio_only)

def save_links_to_file(playlist_url, file_path):
    video_links = get_video_links(playlist_url)
    with open(file_path, 'w') as file:
        for link in video_links:
            file.write(f"{link}\n")
    print(f"{Colors.GREEN}Links saved to {file_path}{Colors.RESET}")

def main():
    # Print the banner
    print_banner()

    # Set up argument parser
    parser = argparse.ArgumentParser(description='Download YouTube videos or playlists.')
    parser.add_argument('url', help='YouTube video or playlist URL or file containing links')
    parser.add_argument('--audio', action='store_true', help='Download only the audio of the video')
    parser.add_argument('--format', choices=['mp4', 'mp3'], default='mp4', help='Specify the format for download')
    parser.add_argument('--file', help='Path to a file containing video or playlist links')
    parser.add_argument('--save-links', help='File path to save links from the playlist')

    args = parser.parse_args()

    if args.save_links:
        save_links_to_file(args.url, args.save_links)
    elif args.file:
        download_videos_from_file(args.file, audio_only=args.audio)
    elif 'playlist' in args.url:
        download_videos_from_playlist(args.url, audio_only=args.audio)
    else:
        download_video(args.url, audio_only=args.audio)

if __name__ == "__main__":
    main()

# generate the list of videos from a playlist link
# add the option to pass a file containing video links (audio or video)
# add the option to pass a file containing playlist links (audio or video)
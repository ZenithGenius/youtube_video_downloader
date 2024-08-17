<<<<<<< HEAD
# youtube_video_downloader
A Python script for downloading YouTube videos and playlists with options for resolution and audio-only formats.
=======
# YouTube Video Downloader

A Python script for downloading YouTube videos and playlists with options for resolution and audio-only formats.

## Features

- Download videos from YouTube playlists or individual video links.
- Automatically selects the highest available resolution up to 1080p.
- Option to download only the audio of the video.
- Colorful terminal output with progress bars and a banner display.

## Prerequisites

- Python 3.7 or higher
- Virtual environment (optional but recommended)

## Installation

### 1. Clone the repository

`git clone <repository-url>`

`cd <repository-directory>`

### 2. Create and activate a virtual environment

#### For Windows:

`python3 -m venv venv`

`venv\Scripts\activate`

#### For macOS/Linux:

`python3 -m venv venv`

`soutce venv\Scripts\activate`

### 3. Install dependencies

Run the following command to install required Python packages:
`pip3 install -r requirements.txt`

### 4. Run the installation script

Alternatively, you can use the install.py script to set up the environment and install dependencies:

`python3 install.py`

## Usage

You can use the script from the command line with various options:

`python3 youtube_downloader.py <URL> [options]`

### Arguments

**url**: The YouTube video or playlist URL.

**-h** or **--help** : Shows the help message and exit.

**--audio**: Download only the audio of the video (applies only if downloading a single video).

**--format**: Specify the format for download. Options are mp4 (default) and mp3.`

### Example

#### Download a single video:

`python3 youtube_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ`

#### Download a single video in audio format:

`python3 youtube_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --audio`

#### Download all videos from a playlist:

`python3 youtube_downloader.py https://www.youtube.com/playlist?list=PL9fPq3eQfaaAGKQQz-du1udbmRehqUDIL`

#### Download all videos from a playlist in audio format:

`python3 youtube_downloader.py https://www.youtube.com/playlist?list=PL9fPq3eQfaaAGKQQz-du1udbmRehqUDIL --audio`
`

### Author


- **Hackwrld** - [*GitHub Profile*](https://github.com/ZenithGenius)

Feel free to open an issue or submit a pull request if you have any suggestions or improvements!
>>>>>>> c2acbab (Initial commit)

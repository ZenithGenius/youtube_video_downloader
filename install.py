import os
import subprocess
import sys

def create_virtualenv(env_name):
    """Create a virtual environment."""
    if not os.path.exists(env_name):
        subprocess.check_call([sys.executable, '-m', 'venv', env_name])
        print(f'Virtual environment {env_name} created.')
    else:
        print(f'Virtual environment {env_name} already exists.')

def install_requirements(env_name, requirements_file):
    """Install the requirements from the requirements file."""
    pip_path = os.path.join(env_name, 'bin', 'pip')
    subprocess.check_call([pip_path, 'install', '--upgrade', 'pip'])
    subprocess.check_call([pip_path, 'install', '-r', requirements_file])
    print(f'Requirements installed from {requirements_file}.')

def main():
    env_name = 'venv'
    requirements_file = 'requirements.txt'
    
    create_virtualenv(env_name)
    install_requirements(env_name, requirements_file)
    
if __name__ == "__main__":
    main()

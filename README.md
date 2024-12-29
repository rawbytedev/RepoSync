# RepoSync

**RepoSync** is a powerful utility designed to effortlessly sync and download files from GitHub repositories. RepoSync intelligently sorts files by size, downloads them seamlessly with support for resuming interrupted downloads, and saves your progress to ensure smooth continuation even after a disconnection. Perfect for developers and teams who need reliable, efficient, and resumable file synchronization from GitHub.

## Features

- **Intelligent Sorting**: Downloads files from smallest to largest.
- **Resume Capability**: Supports pausing and resuming downloads.
- **Progress Tracking**: Saves download state to ensure smooth continuation.
- **Handles Disconnections**: Continues downloads from the last saved point.

## Installation

1. **Clone the Repository**

    ```sh
    git clone https://github.com/rawbytedev/RepoSync.git
    cd RepoSync
    ```
2. **Install Requirements**

    ```sh
    pip install -r requirements.txt
    ```
## Usage
1. **Run the Download Script**

    ```sh
    python reposync.py
    ```
2. **Follow the Prompts**

- Enter the GitHub repository URL.

- Optionally, enter your GitHub access token if the repository is private.

3. **Pause and Resume**

    The script automatically saves the state in download_state.json. To resume, simply run the script again.

## Directory Structure
```RepoSync/
├── download_state.json       # File to save the download state
├── downloads/                # Directory where files are downloaded
├── reposync.py               # Main script for downloading files
└── requirements.txt          # List of required Python packages
```
## Contributing
1. Fork the repository.

2. Create a new branch (git checkout -b feature-branch).

3. Commit your changes (git commit -am 'Add new feature').

4. Push to the branch (git push origin feature-branch).

5. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

If you have any issues or feature requests, feel free to open an issue or contribute to the project.

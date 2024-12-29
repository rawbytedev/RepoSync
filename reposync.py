import os
import requests
import json

# State files to save map creation and download progress
MAP_STATE_FILE = 'map_state.json'
DOWNLOAD_STATE_FILE = 'download_state.json'
CHUNK_SIZE = 100 * 1024  # 100 KB

# Function to get the list of files and folders in the repository
def get_repo_contents(repo_owner, repo_name, path="", access_token=None):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}'
    headers = {
        'Authorization': f'token {access_token}' if access_token else ''
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    contents = response.json()
    return contents

# Function to save the map state
def save_map_state(state):
    with open(MAP_STATE_FILE, 'w') as f:
        json.dump(state, f)

# Function to load the map state
def load_map_state():
    if os.path.exists(MAP_STATE_FILE):
        with open(MAP_STATE_FILE, 'r') as f:
            return json.load(f)
    return {'download_paths': [], 'save_paths': [], 'processed_dirs': []}

# Function to recursively traverse repository and get all files and their paths
def create_repo_map(repo_owner, repo_name, path="", access_token=None):
    state = load_map_state()
    download_paths = state['download_paths']
    save_paths = state['save_paths']
    processed_dirs = state['processed_dirs']

    if path not in processed_dirs:
        contents = get_repo_contents(repo_owner, repo_name, path, access_token)
        for item in contents:
            if item['type'] == 'file':
                download_paths.append(item['download_url'])
                save_paths.append(item['path'])
                print(f"Added file to map: {item['path']}")
            elif item['type'] == 'dir':
                print(f"Entering directory: {item['path']}")
                sub_download_paths, sub_save_paths = create_repo_map(repo_owner, repo_name, item['path'], access_token)
                download_paths.extend(sub_download_paths)
                save_paths.extend(sub_save_paths)
        processed_dirs.append(path)
        save_map_state({'download_paths': download_paths, 'save_paths': save_paths, 'processed_dirs': processed_dirs})

    return download_paths, save_paths

# Function to download a file with resume capability
def download_file(url, local_path, file_size, start_byte=0):
    headers = {
        'Range': f'bytes={start_byte}-'
    }
    try:
        # If file is small, download it directly
        if file_size < CHUNK_SIZE:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return

        # Otherwise, download in chunks
        while start_byte < file_size:
            end_byte = min(start_byte + CHUNK_SIZE - 1, file_size - 1)
            headers = {'Range': f'bytes={start_byte}-{end_byte}'}
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()
            with open(local_path, 'ab') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            start_byte = end_byte + 1

        print(f"Download completed for {url}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

# Function to save the download state
def save_download_state(state):
    with open(DOWNLOAD_STATE_FILE, 'w') as f:
        json.dump(state, f)

# Function to load the download state
def load_download_state():
    if os.path.exists(DOWNLOAD_STATE_FILE):
        with open(DOWNLOAD_STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

# Main function to download files
def download_files(repo_owner, repo_name, access_token=None):
    state = load_download_state()
    download_paths, save_paths = create_repo_map(repo_owner, repo_name, access_token=access_token)

    for download_url, save_path in zip(download_paths, save_paths):
        file_info = requests.head(download_url).headers
        file_size = int(file_info.get('Content-Length', 0))
        local_path = os.path.join('downloads', save_path)
        
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        if save_path in state:
            downloaded_size = state[save_path]['downloaded_size']
        else:
            downloaded_size = 0
        
        print(f'Downloading {save_path} ({downloaded_size}/{file_size} bytes)')
        download_file(download_url, local_path, file_size, start_byte=downloaded_size)
        
        state[save_path] = {'downloaded_size': file_size}
        save_download_state(state)

# Function to extract repo owner and name from URL
def extract_repo_details(repo_url):
    url_parts = repo_url.rstrip('/').split('/')
    if len(url_parts) < 2 or 'github.com' not in url_parts:
        raise ValueError("Invalid GitHub repository URL")
    return url_parts[-2], url_parts[-1]

# Run the download process
if __name__ == '__main__':
    repo_url = input("Enter the GitHub repository URL: ").strip()
    if not repo_url:
        print("Error: GitHub repository URL cannot be empty.")
        exit(1)
    
    access_token = input("Enter your GitHub access token (leave blank if not needed): ").strip() or None
    
    try:
        repo_owner, repo_name = extract_repo_details(repo_url)
        download_files(repo_owner, repo_name, access_token)
    except Exception as e:
        print(f"Error: {e}")
        

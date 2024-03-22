import os
import requests
import sys
import mimetypes
import urllib3

urllib3.disable_warnings()

IGNORE = [
    ".DS_Store",
    "Thumbs.db",
]

BACKEND = "https://aws-us-east-2-1.nuclia.cloud/api/v1"
KNOWLEDGE_BOX = "/kb/f08a00d7-4348-4730-9b77-7fa0bc21851c"
API_KEY = "API_TOKEN"

def upload_file(content_path):
    file_name = os.path.basename(content_path).encode('ascii')
    file_upload_path = f'{BACKEND}{KNOWLEDGE_BOX}/upload'
    print(f'Importing {content_path} at {file_upload_path}')

    with open(content_path, "rb") as source_file:
        response = requests.post(
            file_upload_path,
            headers={
                "content-type": mimetypes.guess_type(content_path)[0] or "application/octet-stream",
                "x-filename": file_name,
                "X-NUCLIA-SERVICEACCOUNT": "Bearer " + API_KEY,
                "x-synchronous": "true",
            },
            data=source_file.read(),
            verify=False,
        )
        if response.status_code != 201:
            print(f'Error {response.status_code} importing {file_name}')

def upload_folder(path):
    all_files = os.listdir(path)
    for content in all_files:
        if content in IGNORE or content.startswith("."):
            continue
        content_path = os.path.join(path, content)
        if os.path.isdir(content_path):
            upload_folder(content_path)
        else:
            upload_file(content_path)

if __name__ == "__main__":
    root = sys.argv[1]
    upload_folder(root)
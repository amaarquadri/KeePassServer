#!/home/amaar/KeePassServer/venv/bin/python
import os
from datetime import datetime
from pathlib import Path
import json
import hashlib
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


FOLDER = Path(__file__).parent.absolute()
KEE_PASS_FILE = os.path.join(FOLDER, 'MasterKeePassDatabase.kdbx')
HASH_FILE = os.path.join(FOLDER, 'kee_pass_hash.txt')
GOOGLE_AUTH_CREDENTIALS_FILE = os.path.join(FOLDER, 'google_auth_credentials.json')
GOOGLE_DRIVE_CONFIG_FILE = os.path.join(FOLDER, 'google_drive_config.json')
LOG_FILE = os.path.join(FOLDER, 'log.txt')


def hash_file(path=KEE_PASS_FILE, block_size=65536):
    hash_function = hashlib.sha256()
    with open(path, 'rb') as file:
        block = file.read(block_size)
        while len(block) > 0:
            hash_function.update(block)
            block = file.read(block_size)
    return hash_function.hexdigest()


def upload_to_drive():
    g_login = GoogleAuth()
    g_login.LoadCredentialsFile(GOOGLE_AUTH_CREDENTIALS_FILE)
    if g_login.credentials is None:
        with open(LOG_FILE, 'a') as fout:
            fout.write(f'{datetime.now()} - No Credentials!\n')
        raise Exception('No Credentials!\n')
    elif g_login.access_token_expired:
        with open(LOG_FILE, 'a') as fout:
            g_login.Refresh()
            fout.write(f'{datetime.now()} - Refreshed Credentials\n')
    drive = GoogleDrive(g_login)

    with open(GOOGLE_DRIVE_CONFIG_FILE, 'r') as fin:
        config = json.load(fin)
    file_drive = drive.CreateFile({'id': config['kee_pass_file_id']})
    file_drive.SetContentFile(KEE_PASS_FILE)
    file_drive.Upload()
    with open(LOG_FILE, 'a') as fout:
        fout.write(f'{datetime.now()} - Upload completed\n')


def main():
    if os.path.isfile(HASH_FILE):
        with open(HASH_FILE, 'r') as fin:
            current_hash = fin.read()
    else:
        current_hash = ""
    new_hash = hash_file()

    if new_hash != current_hash:
        upload_to_drive()
        with open(HASH_FILE, 'w') as fout:
            fout.write(new_hash)


if __name__ == '__main__':
    main()

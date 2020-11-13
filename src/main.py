from time import time
import hashlib
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


KEE_PASS_FILE = 'MasterKeePassDatabase.kdbx'
HASH_FILE = 'keepass_hash.txt'
GOOGLE_AUTH_CREDENTIALS_FILE = 'google_auth_credentials.json'


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
        with open('log.txt', 'a') as fout:
            fout.write('No Credentials!\n')
        raise Exception('No Credentials!\n')
    elif g_login.access_token_expired:
        with open('log.txt', 'a') as fout:
            fout.write('Trying to refresh\n')
            g_login.Refresh()
            fout.write('Tried refreshing\n')
    drive = GoogleDrive(g_login)

    file_drive = drive.CreateFile({'title': KEE_PASS_FILE})
    file_drive.SetContentFile(KEE_PASS_FILE)
    file_drive.Upload()
    with open('log.txt', 'a') as fout:
        fout.write('Upload completed\n')


def main():
    with open(HASH_FILE, 'r') as fin:
        current_hash = fin.read()
    new_hash = hash_file()

    if new_hash != current_hash:
        upload_to_drive()
        with open(HASH_FILE, 'w') as fout:
            fout.write(new_hash)
    else:
        with open('log.txt', 'a') as fout:
            fout.write('No change\n')


if __name__ == '__main__':
    main()

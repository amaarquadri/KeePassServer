import hashlib
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


KEE_PASS_FILE = 'MasterKeePassDatabase.kdbx'
HASH_FILE = 'keepass_hash.txt'


def hash_file(path=KEE_PASS_FILE, block_size=65536):
    hash_function = hashlib.sha256()
    with open(path, 'rb') as file:
        block = file.read(block_size)
        while len(block) > 0:
            hash_function.update(block)
            block = file.read(block_size)
    return hash_function.hexdigest()


def upload_to_drive():
    print('Need to upload')
    g_login = GoogleAuth()
    g_login.LocalWebserverAuth()
    drive = GoogleDrive(g_login)

    file_drive = drive.CreateFile({'title': KEE_PASS_FILE})
    file_drive.SetContentFile(KEE_PASS_FILE)
    file_drive.Upload()


def main():
    with open(HASH_FILE, 'r') as fin:
        current_hash = fin.read()
    new_hash = hash_file()

    if new_hash != current_hash:
        upload_to_drive()
        with open(HASH_FILE, 'w') as fout:
            fout.write(new_hash)


if __name__ == '__main__':
    main()

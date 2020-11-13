from src.main import GOOGLE_AUTH_CREDENTIALS_FILE
from pydrive.auth import GoogleAuth


def main():
    g_login = GoogleAuth()
    g_login.LocalWebserverAuth()
    g_login.SaveCredentialsFile(GOOGLE_AUTH_CREDENTIALS_FILE)


if __name__ == '__main__':
    main()

# KeePass Server
A program to facilitate managing a KeePass server which needs to upload to Google Drive whenever a change is detected.

## Getting Started
- Follow this guide to create a **client_secrets.json** file: https://pythonhosted.org/PyDrive/quickstart.html
- Copy the file to **src/client_secrets.json**
- run the following command to save you Google Auth credentials to a local file: **python src/initialize_credentials.py**
- Find the file id for your KeePass database file from the share link for that file. For example, if the link is
**https://drive.google.com/file/d/1234abc/view?usp=sharing** then the file id is **1234abc**
- Create a file called **google_drive_config.json** in the src folder with the file id as follows:  
{
  "kee_pass_file_id": "1234abc"
}

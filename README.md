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

## Connecting to the Server Using VSFTPD on Linux
If the server is running on a Linux machine that is running on an IP address that is linked to a URL and you want to be able to access the KeePass database from other computers, follow these instructions.
- Update the Linux machine with this command: ```sudo apt update && sudo apt upgrade```.
- Install VSFTPD on the Linux Server with this command: ```sudo apt install vsftpd```.
- Ensure the following settings are enabled in **/etc/vsftpd.conf**:
```
local_enable=YES
write_enable=YES
pasv_enable=YES
pasv_min_port=10100
pasv_max_port=10105  # You can add more or less ports depending on how many people you expect to be connecting at once
pasv_addr_resolve=YES
pasv_addr_resolve=www.example.com  # Enter the URL that resolves to your Linux machine's public IP address here
```
- After updating these settings, make sure to restart the vsftpd service with ```sudo service vsftpd restart```.
- If you have a firewall, ensure that ports 20 and 21 (which are used for ftp) as well as the ports from ```pasv_min_port``` to ```pasv_max_port``` are accessible. For example, if you are using ufw you can do this with the following 2 commands:
```
sudo ufw allow from any to any proto tcp port 20:21
sudo ufw allow from any to any proto tcp port 10100:10105
```
- In KeePass, pick File -> Open -> Open URL. For the URL enter ```ftp://www.example.com/KeePassServer/src/MasterKeePassDatabase.kdbx``` making sure to substitute your URL and update the path after the URL if this repo is not in your home directory. Use the login credentials for the Linux server's user.

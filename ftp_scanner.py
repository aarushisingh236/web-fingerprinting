# ftp_scanner.py
# ----------------------------------------
# FTP Banner Grabbing (Port 21)
# ----------------------------------------

import socket

def grab_ftp_banner(host):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)

        s.connect((host, 21))

        banner = s.recv(1024).decode(errors='ignore')
        s.close()

        return banner

    except Exception as e:
        return f"FTP Error: {e}"
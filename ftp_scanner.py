# ftp_scanner.py
# ----------------------------------------
# FTP Banner Grabbing (Port 21)
# ----------------------------------------

import socket

def scan_ftp(host):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(7)  # Increased timeout for robustness

        s.connect((host, 21))

        # Some FTP servers have a slight delay before sending the banner
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()

        return banner if banner else "FTP Connection established (No Banner)"

    except Exception as e:
        return f"FTP Error: {e}"

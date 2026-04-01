# http_scanner.py
# ----------------------------------------
# HTTP Banner Grabbing (Port 80)
# Uses TCP socket to send HEAD request
# ----------------------------------------

import socket

def grab_http_banner(host):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)

        s.connect((host, 80))

        request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\n\r\n"
        s.send(request.encode())

        response = s.recv(4096).decode(errors='ignore')
        s.close()

        return response

    except Exception as e:
        return f"HTTP Error: {e}"
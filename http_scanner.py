# http_scanner.py
# ----------------------------------------
# HTTP Banner Grabbing (Port 80)
# Uses TCP socket to send HEAD request
# ----------------------------------------

import socket

def scan_http(host):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(7)  # Increased timeout for robustness

        s.connect((host, 80))

        # Improved request with User-Agent and specific headers
        request = (
            f"HEAD / HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) FingerprintingTool/1.0\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )
        s.send(request.encode())

        response = s.recv(4096).decode(errors='ignore')
        s.close()

        return response

    except Exception as e:
        return f"HTTP Error: {e}"

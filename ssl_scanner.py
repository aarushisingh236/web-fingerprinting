# ssl_scanner.py
# ----------------------------------------
# HTTPS Banner Grabbing (Port 443)
# Uses HEAD + GET fallback (IMPORTANT)
# ----------------------------------------

import socket
import ssl

def grab_https_banner(host):
    try:
        context = ssl.create_default_context()

        sock = socket.create_connection((host, 443), timeout=3)
        ssock = context.wrap_socket(sock, server_hostname=host)

        # ---- HEAD request ----
        request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        ssock.send(request.encode())

        response = b""
        while True:
            chunk = ssock.recv(4096)
            if not chunk:
                break
            response += chunk

        response = response.decode(errors='ignore')

        # ---- If weak response → try GET ----
        if len(response) < 300:
            sock = socket.create_connection((host, 443), timeout=3)
            ssock = context.wrap_socket(sock, server_hostname=host)

            request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            ssock.send(request.encode())

            response = b""
            while True:
                chunk = ssock.recv(4096)
                if not chunk:
                    break
                response += chunk

            response = response.decode(errors='ignore')
            ssock.close()

        return response

    except Exception as e:
        return f"HTTPS Error: {e}"
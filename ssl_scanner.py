# tls_scanner.py
# ----------------------------------------
# HTTPS Banner Grabbing using TLS (explicit)
# Enforces TLS 1.2+ (modern secure setup)
# HTTPS Banner Grabbing (Port 443)
# ----------------------------------------

import socket
import ssl

def scan_https(host):
    try:
        # ---- Create TLS context explicitly ----
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_default_certs()

        # ---- TCP connection ----
        sock = socket.create_connection((host, 443), timeout=3)

        # ---- TLS handshake ----
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

        # ---- Fallback to GET ----
        if len(response) < 300:
            ssock.close()

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
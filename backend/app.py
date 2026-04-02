import sys
import os
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import json
import time

# Add the parent directory to sys.path to import scanners
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from http_scanner import scan_http
from ftp_scanner import scan_ftp
from ssl_scanner import scan_https
from fingerprint_logic import identify_server, extract_server_header

app = Flask(__name__)
CORS(app)

@app.route('/api/scan', methods=['POST'])
def scan_targets():
    data = request.json
    targets = data.get('targets', [])

    def generate():
        for i, target in enumerate(targets):
            # Send initial progress for each target
            yield f"data: {json.dumps({'status': 'scanning', 'target': target, 'index': i})}\n\n"
            
            try:
                # --- Scanning with detailed status ---
                https_banner = scan_https(target)
                https_ok = https_banner and not https_banner.startswith("HTTPS Error")
                
                http_banner = scan_http(target)
                http_ok = http_banner and not http_banner.startswith("HTTP Error")
                
                ftp_banner = scan_ftp(target)
                ftp_ok = ftp_banner and (ftp_banner.startswith("220") or "Connection established" in ftp_banner)

                # --- Selection Logic (Sync with main.py) ---
                if https_ok:
                    selected_banner = https_banner
                    source = "HTTPS"
                elif http_ok:
                    selected_banner = http_banner
                    source = "HTTP"
                elif ftp_ok:
                    selected_banner = ftp_banner
                    source = "FTP"
                else:
                    selected_banner = f"{https_banner}\n{http_banner}\n{ftp_banner}"
                    source = "None (Unified Error)"

                server = identify_server(selected_banner, target)
                server_header = extract_server_header(selected_banner)

                result = {
                    "status": "done",
                    "host": target,
                    "server_type": server,
                    "server_header": server_header,
                    "source": source,
                    "index": i,
                    "protocols": {
                        "https": {"ok": bool(https_ok), "msg": "SUCCESS" if https_ok else https_banner},
                        "http": {"ok": bool(http_ok), "msg": "SUCCESS" if http_ok else http_banner},
                        "ftp": {"ok": bool(ftp_ok), "msg": "SUCCESS" if ftp_ok else ftp_banner}
                    }
                }
                yield f"data: {json.dumps(result)}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'status': 'error', 'host': target, 'message': str(e), 'index': i})}\n\n"
            
            # Small delay for visual feel (optional, but good for local dev)
            # time.sleep(0.5)

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
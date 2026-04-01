import sys
import os
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
import json
import time

# Add the parent directory to sys.path to import scanners
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from http_scanner import grab_http_banner
from ftp_scanner import grab_ftp_banner
from ssl_scanner import grab_https_banner
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
                https_banner = grab_https_banner(target)
                http_banner = grab_http_banner(target)
                ftp_banner = grab_ftp_banner(target)

                # --- Selection Logic (from main.py) ---
                if https_banner and not https_banner.startswith("HTTPS Error"):
                    selected_banner = https_banner
                    source = "HTTPS"
                elif http_banner and not http_banner.startswith("HTTP Error"):
                    selected_banner = http_banner
                    source = "HTTP"
                elif ftp_banner and ftp_banner.startswith("220"):
                    selected_banner = ftp_banner
                    source = "FTP"
                else:
                    selected_banner = (https_banner or "") + (http_banner or "") + (ftp_banner or "")
                    source = "Combined (fallback)"

                server = identify_server(selected_banner, target)
                server_header = extract_server_header(selected_banner)

                result = {
                    "status": "done",
                    "host": target,
                    "server_type": server,
                    "server_header": server_header,
                    "source": source,
                    "index": i
                }
                yield f"data: {json.dumps(result)}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'status': 'error', 'host': target, 'message': str(e), 'index': i})}\n\n"
            
            # Small delay for visual feel (optional, but good for local dev)
            # time.sleep(0.5)

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
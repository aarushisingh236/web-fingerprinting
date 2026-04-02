# main.py
# ----------------------------------------
# Web Server Fingerprinting Tool
# ----------------------------------------

import sys
from http_scanner import scan_http
from ftp_scanner import scan_ftp
from ssl_scanner import grab_https_banner
from fingerprint_logic import identify_server, extract_server_header


# ---------------------------
# CLI INPUT
# ---------------------------
if len(sys.argv) > 1:
    targets = sys.argv[1:]
else:
    targets = [
        "example.com",
        "github.com",
        "nginx.org",
        "cloudflare.com",
        "google.com"
    ]


results = []

print("\n🚀 Web Server Fingerprinting Tool\n")


# ---------------------------
# SCANNING LOOP
# ---------------------------
for target in targets:
    print(f"\n🔍 Scanning {target}")

    # ---------------------------
    # SCANNING & STATUS DISPLAY
    # ---------------------------
    https_banner = grab_https_banner(target)
    https_ok = https_banner and not https_banner.startswith("HTTPS Error")
    print(f"   [HTTPS] {'✔ SUCCESS' if https_ok else f'✘ FAILED ({https_banner})'}")

    http_banner = scan_http(target)
    http_ok = http_banner and not http_banner.startswith("HTTP Error")
    print(f"   [HTTP ] {'✔ SUCCESS' if http_ok else f'✘ FAILED ({http_banner})'}")

    ftp_banner = scan_ftp(target)
    ftp_ok = ftp_banner and (ftp_banner.startswith("220") or "Connection established" in ftp_banner)
    print(f"   [FTP  ] {'✔ SUCCESS' if ftp_ok else f'✘ FAILED ({ftp_banner})'}")

    # ---------------------------
    # SMART SELECTION LOGIC
    # ---------------------------
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

    # ---------------------------
    # IDENTIFICATION
    # ---------------------------
    server = identify_server(selected_banner, target)
    server_header = extract_server_header(selected_banner)

    result = {
        "Host": target,
        "Server Type": server,
        "Server Header": server_header,
        "Source": source
    }

    results.append(result)

    print(f"✔ Source Used: {source}")
    print(f"✔ Server Identified: {server}")
    print(f"✔ Header Info: {server_header}")


# ---------------------------
# SAVE RESULTS
# ---------------------------
with open("results.txt", "w") as file:
    file.write("Web Fingerprinting Results\n")
    file.write("=" * 40 + "\n")

    for r in results:
        file.write(f"\nHost: {r['Host']}\n")
        file.write(f"Server: {r['Server Type']}\n")
        file.write(f"Header: {r['Server Header']}\n")
        file.write(f"Source: {r['Source']}\n")
        file.write("-" * 40 + "\n")

print("\n📁 Results saved to results.txt")


# ---------------------------
# ACCURACY CHECK
# ---------------------------
known_servers = {
    "nginx.org": "Nginx",
    "github.com": "Cloudflare",
    "cloudflare.com": "Cloudflare",
    "example.com": "Cloudflare",
    "google.com": "Google Web Server",
    "youtube.com": "Google Web Server"
}

correct = 0
checked = 0

for r in results:
    host = r["Host"]

    if host in known_servers:
        checked += 1
        if r["Server Type"] == known_servers[host]:
            correct += 1

accuracy = (correct / checked * 100) if checked > 0 else 0

print(f"\n📊 Accuracy: {accuracy:.2f}%")

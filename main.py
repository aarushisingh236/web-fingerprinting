# main.py
# ----------------------------------------
# Web Server Fingerprinting Tool
# ----------------------------------------

import sys
from http_scanner import grab_http_banner
from ftp_scanner import grab_ftp_banner
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

    https_banner = grab_https_banner(target)
    http_banner = grab_http_banner(target)
    ftp_banner = grab_ftp_banner(target)

    # ---------------------------
    # SMART SELECTION LOGIC
    # ---------------------------
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
        selected_banner = https_banner + http_banner + ftp_banner
        source = "Combined (fallback)"

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
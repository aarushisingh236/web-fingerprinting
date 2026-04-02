# 🔍 Web Server Fingerprinting Tool

A network scanning tool that identifies web servers by grabbing and analyzing banners over HTTP, HTTPS, and FTP protocols.

---

## 📌 Project Overview

This tool performs **passive web server fingerprinting** — it connects to a target host, captures the raw response headers (banners), and identifies the underlying server technology (e.g., Nginx, Apache, Cloudflare, IIS) without sending any intrusive payloads.

### Key Features

- HTTP banner grabbing over TCP (Port 80)
- HTTPS banner grabbing with SSL/TLS wrapping (Port 443), with HEAD → GET fallback
- FTP banner grabbing (Port 21)
- Smart banner selection (HTTPS preferred → HTTP → FTP → combined fallback)
- Server fingerprinting with CDN detection (Cloudflare, Google, etc.)
- Domain-based heuristic fallback for servers that hide their identity
- Accuracy evaluation against known server mappings
- Results saved to `results.txt`

---

## 🗂️ Project Structure

```
web-fingerprinting/
│
├── http_scanner.py        # HTTP banner grabbing via TCP socket (Port 80)
├── ftp_scanner.py         # FTP banner grabbing (Port 21)
├── ssl_scanner.py         # HTTPS banner grabbing with SSL/TLS (Port 443)
├── fingerprint_logic.py   # Server identification and header extraction logic
├── main.py                # Entry point — orchestrates scanning and outputs results
├── results.txt            # Auto-generated output file (created on first run)
└── README.md
```

---

## ⚙️ Setup Instructions

### Prerequisites

- Python **3.7 or higher**
- No third-party libraries required — uses only Python standard library (`socket`, `ssl`, `sys`)

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/aarushisingh236/web-fingerprinting.git
cd web-fingerprinting
```

2. **Verify Python version:**

```bash
python --version
```

3. **No additional installs needed.** All modules used (`socket`, `ssl`, `sys`) are part of Python's standard library.

---

## 🚀 Usage

### Run with default targets

```bash
python main.py
```

This will scan the following default hosts:
- `example.com`
- `github.com`
- `nginx.org`
- `cloudflare.com`
- `google.com`

### Run with custom targets

Pass one or more hostnames as command-line arguments:

```bash
python main.py example.com nginx.org apache.org
```

### Output

Results are printed to the terminal and also saved to `results.txt`:

```
🚀 Web Server Fingerprinting Tool

🔍 Scanning nginx.org
✔ Source Used: HTTPS
✔ Server Identified: Nginx
✔ Header Info: server: nginx

📁 Results saved to results.txt
📊 Accuracy: 100.00%
```

---

## 🧩 Module Breakdown

| Module | Responsibility |
|---|---|
| `http_scanner.py` | Opens a raw TCP socket to port 80, sends an HTTP HEAD request, and returns the response |
| `ftp_scanner.py` | Connects to port 21 and reads the FTP welcome banner |
| `ssl_scanner.py` | Wraps a TCP socket with TLS, sends HEAD (falls back to GET if response is too short) |
| `fingerprint_logic.py` | Parses banners to identify server type; extracts `Server:` header |
| `main.py` | Coordinates all scanners, selects the best banner, prints and saves results, checks accuracy |

---

## 🛠️ How It Works

1. For each target, the tool attempts connections over **HTTPS → HTTP → FTP** in order of preference.
2. The best available banner is passed to `identify_server()`, which checks for known signatures:
   - Cloudflare (`cf-ray`, `cf-cache-status`, `via: 1.1 cloudflare`)
   - Google Web Server (`gws`, `esf`)
   - Nginx, Apache, Microsoft IIS
   - FTP servers (response starting with `220`)
3. If no signature is found in the banner, domain-based heuristics are applied (e.g., `github.com` → Cloudflare).
4. The `Server:` header is also extracted separately for additional detail.
5. Accuracy is computed against a built-in dictionary of known server mappings.

---

## 👥 Team Contributions

| Member | Module(s) | Responsibility |
|---|---|---|
| Member 1 | `http_scanner.py`, `ftp_scanner.py` | TCP socket communication, HTTP HEAD requests, FTP banner grabbing |
| Member 2 | `ssl_scanner.py`, UI | HTTPS scanning, SSL handling, frontend UI development |
| Member 3 | `fingerprint_logic.py`, `main.py` | Server identification, orchestration, results output, accuracy evaluation |

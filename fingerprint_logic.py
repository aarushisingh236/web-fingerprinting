# fingerprint_logic.py
# ----------------------------------------
# FINAL fingerprinting logic
# Includes:
# - Banner detection
# - CDN detection
# - Domain-based fallback (important)
# - False-positive prevention
# ----------------------------------------

def identify_server(banner, host=""):
    # Handle empty banner safely
    if not banner:
        banner = ""

    banner = banner.lower()
    host = host.lower()

    # -------- CLOUDFARE DETECTION --------
    if (
        "cloudflare" in banner or
        "cf-ray" in banner or
        "cf-cache-status" in banner or
        "via: 1.1 cloudflare" in banner
    ):
        return "Cloudflare"

    # -------- GOOGLE SERVERS --------
    # GWS (Google Web Server) and ESF (Edge Server)
    elif "gws" in banner or "esf" in banner:
        return "Google Web Server"

    # -------- COMMON SERVERS --------
    elif "nginx" in banner:
        return "Nginx"

    elif "apache" in banner:
        return "Apache"

    # -------- MICROSOFT IIS (STRICT MATCH) --------
    elif "server: microsoft-iis" in banner:
        return "Microsoft IIS"

    # -------- FTP --------
    elif banner.startswith("220"):
        return "FTP Server"

    # -------- FALLBACK HEURISTICS --------
    # Known CDN-backed domains
    elif "github.com" in host:
        return "Cloudflare"

    return "Unknown"


def extract_server_header(banner):
    """
    Extracts 'Server' header from HTTP/HTTPS response.
    """

    if not banner:
        return "Server header not found"

    for line in banner.split("\n"):
        if "server:" in line.lower():
            return line.strip()

    return "Server header not found"
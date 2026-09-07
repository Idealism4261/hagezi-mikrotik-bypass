import urllib.request
from pathlib import Path

SOURCE_URL = (
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/"
    "main/wildcard/doh-vpn-proxy-bypass.txt"
)

OUTPUT_FILE = Path("doh-vpn-proxy-bypass-mikrotik.txt")


def download_source():
    with urllib.request.urlopen(SOURCE_URL, timeout=30) as response:
        return response.read().decode("utf-8")


def convert(data):
    output = []

    for line in data.splitlines():
        line = line.strip()

        # Ignore empty lines and comments
        if not line or line.startswith("#"):
            continue

        # Hagezi wildcard format:
        # *.example.com
        if line.startswith("*."):
            domain = line[2:].strip()

            if domain:
                output.append(f"0.0.0.0 {domain}")

    # Remove duplicates and sort
    return sorted(set(output), key=str.lower)


def main():
    source = download_source()
    entries = convert(source)

    header = [
        "# Hagezi DoH/VPN/TOR/Proxy Bypass list",
        "# Converted to MikroTik Adlist hosts format",
        "# Source: https://github.com/hagezi/dns-blocklists",
        f"# Entries: {len(entries)}",
        "",
    ]

    OUTPUT_FILE.write_text(
        "\n".join(header + entries) + "\n",
        encoding="utf-8",
    )

    print(f"Generated {len(entries)} entries.")


if __name__ == "__main__":
    main()

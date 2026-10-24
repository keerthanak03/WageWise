
"""Download permitted URLs from urls.txt into data/raw/."""

import csv
import hashlib
import os
import re
import sys
import time
from datetime import date
from pathlib import Path
from urllib.parse import urlparse, unquote
from urllib.robotparser import RobotFileParser

import requests

RAW = Path("data/raw")
MANIFEST = Path("data/manifest.csv")
DELAY = 2

HEADERS = {
    "User-Agent": (
        "WageWiseStudentProject/1.0 "
        "(educational project)"
    ),
    "Accept": "text/html,application/pdf,*/*",
}

session = requests.Session()
session.headers.update(HEADERS)
robots = {}


def allowed(url):
    """Check robots.txt before downloading."""
    parsed = urlparse(url)
    root = f"{parsed.scheme}://{parsed.netloc}"

    if root not in robots:
        rp = RobotFileParser()
        rp.set_url(root + "/robots.txt")

        try:
            response = session.get(
                root + "/robots.txt", timeout=15
            )
            if response.status_code == 200:
                rp.parse(response.text.splitlines())
                robots[root] = rp
            else:
                print(
                    "Cannot verify robots.txt for", root,
                    "- skipping this host for safety."
                )
                robots[root] = None
        except requests.RequestException as exc:
            print("Could not check robots.txt:", exc)
            robots[root] = None

    rp = robots[root]

    # If permission cannot be verified, do not download.
    if rp is None:
        return False

    return rp.can_fetch(HEADERS["User-Agent"], url)


def name_for(url, content_type=""):
    """Build a filename from the URL."""
    path_name = unquote(
        Path(urlparse(url).path).name
    )

    if not path_name or "." not in path_name:
        path_name = urlparse(url).path.strip("/").split("/")
        path_name = path_name[-1] if path_name else "document"
        path_name = path_name or "document"

    path_name = re.sub(r'[<>:"/\\|?*]', "_", path_name)

    if "pdf" in content_type.lower():
        if not path_name.lower().endswith(".pdf"):
            path_name += ".pdf"
    elif "html" in content_type.lower():
        if not path_name.lower().endswith((".html", ".htm")):
            path_name += ".html"

    return path_name


def main(list_file):
    RAW.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)

    new_manifest = (
        not MANIFEST.exists() or MANIFEST.stat().st_size == 0
    )

    with MANIFEST.open("a", newline="", encoding="utf-8") as mf:
        log = csv.writer(mf)

        if new_manifest:
            log.writerow([
                "file", "source_url", "downloaded_on",
                "bytes", "sha256"
            ])

        with open(list_file, encoding="utf-8-sig") as fh:
            urls = [
                line.strip()
                for line in fh
                if line.strip() and not line.strip().startswith("#")
            ]

        for url in urls:
            if urlparse(url).scheme not in ("http", "https"):
                print("Invalid URL:", url)
                continue

            if not allowed(url):
                print("Skipped: permission not verified:", url)
                continue

            try:
                response = session.get(
                    url, timeout=30, allow_redirects=True
                )

                if response.status_code != 200:
                    print(
                        "HTTP error:", response.status_code, url
                    )
                    if response.status_code == 403:
                        print(
                            "Access denied. Use an official direct "
                            "download link or download it manually."
                        )
                    continue

                content_type = response.headers.get(
                    "Content-Type", ""
                )

                if not (
                    "pdf" in content_type.lower()
                    or "html" in content_type.lower()
                    or "text/plain" in content_type.lower()
                ):
                    print("Skipped unsupported content:", content_type)
                    continue

                filename = name_for(url, content_type)
                path = RAW / filename

                if path.exists():
                    print("Already exists:", path)
                    continue

                content = response.content

                # Avoid saving an HTML error page as a PDF.
                if "pdf" in content_type.lower() and not content.startswith(b"%PDF-"):
                    print("Response is not a valid PDF:", url)
                    continue

                path.write_bytes(content)
                digest = hashlib.sha256(content).hexdigest()

                log.writerow([
                    str(path),
                    url,
                    date.today().isoformat(),
                    len(content),
                    digest,
                ])
                mf.flush()

                print("Saved:", path, "-", len(content), "bytes")

            except requests.RequestException as exc:
                print("Request failed:", url, "-", exc)

            time.sleep(DELAY)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/download.py urls.txt")
        sys.exit(1)

    main(sys.argv[1])

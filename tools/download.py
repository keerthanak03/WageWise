
"""Download direct PDF URLs and PDFs linked from HTML pages."""

import csv
import hashlib
import re
import sys
import time
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

RAW = Path("data/raw")
MANIFEST = Path("data/manifest.csv")
DELAY = 2

HEADERS = {
    "User-Agent": "WageWiseStudentProject/1.0 (educational project)",
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
            response = session.get(root + "/robots.txt", timeout=15)

            if response.status_code == 200:
                rp.parse(response.text.splitlines())
                robots[root] = rp
            else:
                print("Cannot verify robots.txt:", root)
                robots[root] = None

        except requests.RequestException as exc:
            print("Could not check robots.txt:", exc)
            robots[root] = None

    rp = robots[root]

    if rp is None:
        return False

    return rp.can_fetch(HEADERS["User-Agent"], url)


def find_pdf_links(page_url, html):
    """Find PDF links inside an HTML page."""
    soup = BeautifulSoup(html, "html.parser")
    pdf_links = set()

    for link in soup.find_all("a", href=True):
        pdf_url = urljoin(page_url, link["href"])

        if ".pdf" in urlparse(pdf_url).path.lower():
            pdf_links.add(pdf_url)

    return pdf_links


def save_pdf(url, content):
    """Validate and save a PDF."""
    if not content.startswith(b"%PDF-"):
        print("Not a valid PDF:", url)
        return

    filename = unquote(Path(urlparse(url).path).name)

    if not filename or filename == "/":
        filename = "document.pdf"

    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)

    path = RAW / filename

    # Avoid overwriting files with the same name.
    if path.exists():
        digest_existing = hashlib.sha256(path.read_bytes()).hexdigest()
        digest_new = hashlib.sha256(content).hexdigest()

        if digest_existing == digest_new:
            print("Already downloaded:", path)
            return

        stem = path.stem
        path = RAW / f"{stem}_{digest_new[:8]}.pdf"

    path.write_bytes(content)

    digest = hashlib.sha256(content).hexdigest()

    with MANIFEST.open("a", newline="", encoding="utf-8") as mf:
        log = csv.writer(mf)

        if mf.tell() == 0:
            log.writerow([
                "file",
                "source_url",
                "downloaded_on",
                "bytes",
                "sha256",
            ])

        log.writerow([
            str(path),
            url,
            date.today().isoformat(),
            len(content),
            digest,
        ])

    print("PDF saved:", path)
    time.sleep(DELAY)


def download_pdf(url):
    """Download a direct PDF URL."""
    if not allowed(url):
        print("Skipped: permission not verified:", url)
        return

    try:
        response = session.get(
            url,
            timeout=60,
            allow_redirects=True,
        )

        if response.status_code != 200:
            print("HTTP error:", response.status_code, url)
            return

        content_type = response.headers.get("Content-Type", "").lower()

        if (
            "pdf" in content_type
            or urlparse(response.url).path.lower().endswith(".pdf")
            or response.content.startswith(b"%PDF-")
        ):
            save_pdf(response.url, response.content)
        else:
            print("URL did not return a PDF:", url)

    except requests.RequestException as exc:
        print("Download failed:", url, "-", exc)


def process_url(url):
    """Handle both direct PDFs and HTML listing pages."""

    print("\nChecking URL:", url)

    if not allowed(url):
        print("Skipped: permission not verified:", url)
        return

    try:
        response = session.get(url, timeout=30)

        if response.status_code != 200:
            print("Page error:", response.status_code, url)
            return

        content_type = response.headers.get("Content-Type", "").lower()

        # Case 1: The URL itself is a PDF.
        if (
            "pdf" in content_type
            or response.url.lower().split("?")[0].endswith(".pdf")
            or response.content.startswith(b"%PDF-")
        ):
            save_pdf(response.url, response.content)
            return

        # Case 2: The URL is an HTML listing page.
        if "html" not in content_type:
            print("Unsupported content type:", content_type)
            return

        pdf_links = find_pdf_links(response.url, response.text)

        print("PDF links found:", len(pdf_links))

        for pdf_url in sorted(pdf_links):
            download_pdf(pdf_url)

    except requests.RequestException as exc:
        print("Request failed:", url, "-", exc)


def main(list_file):
    RAW.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)

    with open(list_file, encoding="utf-8-sig") as fh:
        urls = [
            line.strip()
            for line in fh
            if line.strip() and not line.strip().startswith("#")
        ]

    for url in urls:
        process_url(url)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/download.py urls.txt")
        sys.exit(1)

    main(sys.argv[1])

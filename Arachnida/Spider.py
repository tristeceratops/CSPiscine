#!/usr/bin/env python3
import requests
import re
import os
import argparse
from urllib.parse import urljoin, urlparse

# ------------------ utils ------------------

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# ------------------ argparse ------------------

parser = argparse.ArgumentParser(description="Recursive image web scraper")

parser.add_argument("url", help="Target URL to scrape")

parser.add_argument(
    "-r",
    action="store_true",
    help="Enable recursive mode"
)

parser.add_argument(
    "-l",
    type=int,
    help="Recursion depth (default: 5)"
)

parser.add_argument(
    "-p",
    default="downloaded_files",
    help="Downloaded images path"
)

args = parser.parse_args()

if args.l and not args.r:
    parser.error("-l requires -r")

# ------------------ depth logic ------------------

if not args.r:
    depth = 1
elif args.l is None:
    depth = 5
else:
    depth = args.l

# ------------------ setup ------------------

extensions = ['.png', '.jpg', '.jpeg', '.gif', 'bmp']

image_pattern = re.compile(
    r'(?:src|href)=(["\'])(.*?(?:' +
    '|'.join(map(re.escape, extensions)) +
    r'))\1',
    re.IGNORECASE
)

link_pattern = re.compile(
    r'(?:src|href)=(["\'])(.*?)\1',
    re.IGNORECASE
)

HEADERS = {
    "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "fr,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/png,image/jpeg,image/gif,image/bmp",
    "Referer": "https://www.example.com/search",
    "Connection": "keep-alive"
}


save_dir = args.p
os.makedirs(save_dir, exist_ok=True)

# ------------------ recursive scraper ------------------

def scrape_page(url, depth, visited):
    if depth == 0:
        return

    if url in visited:
        return

    visited.add(url)
    print(f"[+] Scraping ({depth}) → {url}")

    try:
        response = requests.get(url, timeout=5, headers=HEADERS)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"[!] Failed to fetch {url}: {e}")
        return

    # ---- download images ----
    images = image_pattern.findall(html)

    for match in images:
        img_url = urljoin(url, match[1])

        try:
            img = requests.get(img_url, stream=True, timeout=5, headers=HEADERS)
            img.raise_for_status()

            filename = os.path.basename(urlparse(img_url).path)
            if not filename:
                continue

            filepath = os.path.join(save_dir, filename)
            if os.path.exists(filepath):
                continue

            with open(filepath, "wb") as f:
                for chunk in img.iter_content(8192):
                    f.write(chunk)

            print(f"    Saved: {filename}")

        except Exception:
            pass

    # ---- recursion ----
    if args.r:
        links = link_pattern.findall(html)

        for link in links:
            next_url = urljoin(url, link[1])
            parsed = urlparse(next_url)

            if parsed.scheme not in ("http", "https"):
                continue

            scrape_page(next_url, depth - 1, visited)

# ------------------ run ------------------

if not is_valid_url(args.url):
    print("Invalid URL:", args.url)
    exit(1)

visited = set()
scrape_page(args.url, depth, visited)
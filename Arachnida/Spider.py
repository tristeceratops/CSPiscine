#!/usr/bin/env python3
import requests
import os
import argparse
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

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
    default="data",
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

extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "fr,en;q=0.9",
    "Accept": "*/*",
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

    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all('img')

    for image in images:
        img_url = image['src']

        try:
            print(f"try with image url: {img_url}")
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

        except Exception as e:
            print(f"Failed to download image at url {img_url}, e: {e}")

    # ---- recursion ----
    if args.r:
        links = soup.find_all('a')

        for link in links:
            next_url = link['href']
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
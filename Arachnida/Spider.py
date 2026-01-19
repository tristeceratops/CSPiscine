#!/usr/bin/env python3
import requests
import os
import argparse
from urllib.parse import urljoin, urlparse, urlencode
from bs4 import BeautifulSoup
from collections import deque

# ------------------ utils ------------------

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_image_url(url):
    path = urlparse(url).path.lower()
    return path.endswith(extensions)


def extract_all_urls(soup):
    urls = set()

    for tag in soup.find_all(True):
        for attr, value in tag.attrs.items():
            if ("srcset" in attr) and isinstance(value, str):
                urls.update(parse_srcset(value))
            elif isinstance(value, str):
                urls.add(value)

    return urls


def parse_srcset(srcset_value):
    urls = []
    for part in srcset_value.split(","):
        url = part.strip().split()[0]
        urls.append(url)
    return urls


def handle_image(img_url):
    path = urlparse(img_url).path
    filename = os.path.basename(path)
    if not filename:
        return

    filepath = os.path.join(save_dir, filename)
    if os.path.exists(filepath):
        # print(f"{img_url} already exist")
        return

    if not path.lower().endswith(extensions):
        return

    try:
        print(f"Try download image: {img_url}")
        img = requests.get(img_url, stream=True, timeout=5, headers=HEADERS)
        img.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in img.iter_content(8192):
                f.write(chunk)

        print(f"Saved: {filename}")

    except Exception as e:
        print(f"Failed: {img_url} → {e}")

def clean_url(raw_url):
    raw_url = raw_url.strip()

    start_idx = raw_url.find("url(")
    if start_idx != -1:
        raw_url = raw_url[start_idx + 4:]
        end_idx = raw_url.find(")")
        if end_idx != -1:
            raw_url = raw_url[:end_idx]

    raw_url = raw_url.strip().rstrip(";").strip()

    return raw_url

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

extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Accept-Language": "fr-FR,en-US;q=0.7,en;q=0.3",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

save_dir = args.p
os.makedirs(save_dir, exist_ok=True)

# ------------------ BFS scraper ------------------
def bfs_scrape(start_url, max_depth):
    visited = set()
    queue = deque([(start_url, max_depth)])

    while queue:
        url, depth = queue.popleft()
        if depth == 0 or url in visited:
            continue

        visited.add(url)
        print(f"[+] Scraping ({depth}) → {url}")

        try:
            response = requests.get(url, timeout=5, headers=HEADERS)
            response.raise_for_status()
            html = response.text
        except Exception as e:
            print(f"[!] Failed to fetch {url}: {e}")
            continue

        soup = BeautifulSoup(html, 'html.parser')

        # ---- handle images ----
        raw_urls = extract_all_urls(soup)
        for raw_url in raw_urls:
            raw_url = clean_url(raw_url)
            img_url = urljoin(url, raw_url)
            if is_image_url(img_url):
                handle_image(img_url)

        # ---- enqueue links for next depth ----
        if args.r:
            links = soup.find_all('a', href=True)
            for link in links:
                next_url = urljoin(url, link['href'])
                parsed = urlparse(next_url)

                if parsed.scheme not in ("http", "https"):
                    continue

                if next_url not in visited:
                    queue.append((next_url, depth - 1))

# ------------------ run ------------------

if not is_valid_url(args.url):
    print("Invalid URL:", args.url)
    exit(1)

visited = set()
bfs_scrape(args.url, depth)
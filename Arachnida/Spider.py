#!/usr/bin/env python3
import requests
import re
import os
import argparse
from urllib.parse import urljoin, urlparse

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

parser = argparse.ArgumentParser(
    description="Image web scraper"
)

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

recursion = args.r
depth = 5
if recursion and args.l:
    depth = args.l

# List of extensions you want to find
extensions = ['.png', '.jpg', '.jpeg', '.gif']

# Fetch the page
url = args.url

if not is_valid_url(url):
    print("Invalid URL:", url)
    exit(1)

response = requests.get(url)
html_content = response.text

# Regex pattern to find image URLs in src or href attributes
pattern = re.compile(
    r'(?:src|href)=(["\'])(.*?(?:' +
    '|'.join(map(re.escape, extensions)) +
    r'))\1',
    re.IGNORECASE
)

# Find all matches
matches = pattern.findall(html_content)

# Extract unique file URLs
files = set()
for match in matches:
    file_url = match[1]
    files.add(file_url)

# Print all found image URLs
save_dir = args.p
os.makedirs(save_dir, exist_ok=True)

# Download and save each file
for file_url in files:
    # Handle relative URLs
    full_url = urljoin(url, file_url)
    try:
        file_response = requests.get(full_url, stream=True)
        file_response.raise_for_status()
        # Extract filename from URL
        filename = os.path.basename(full_url)
        filepath = os.path.join(save_dir, filename)
        # Save the file
        with open(filepath, 'wb') as f:
            for chunk in file_response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Saved: {filepath}")
    except Exception as e:
        print(f"Failed to download {full_url}: {e}")
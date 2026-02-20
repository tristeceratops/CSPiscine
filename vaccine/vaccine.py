import requests
from urllib.parse import urljoin, urlparse, parse_qsl
from pprint import pprint
import argparse
try:
    from ressource.generate.error_patterns import ERROR_PATTERNS
    from ressource.generate.mysql_patterns import MYSQL_ERROR
    from ressource.generate.sqlite_patterns import SQLITE_ERROR
except ImportError as e:
        print("Import of generates modules failed. Please run make before the script")
        print(f"Error: {e}")
        exit(1)

def is_vulnerable_errors(response):
    answer = False
    for errors in ERROR_PATTERNS:
        for error in ERROR_PATTERNS[errors]:
            if error in response.content.decode().lower():
                if not answer:
                    answer = True
                    break
        return answer

def get_insertion_position(query_string, target_key):
    start = query_string.find(target_key + "=")
    if start == -1:
        return None

    value_start = start + len(target_key) + 1
    value_end = query_string.find("&", value_start)

    if value_end == -1:  # last parameter
        return len(query_string)

    return value_end

def test_sqli_errors(url, params):
    found = False

    #MySQL
    sqli_list = MYSQL_ERROR["errors"]
    for parameter, value in params:
        for injection in sqli_list:
            pos = get_insertion_position(url, parameter)
            if pos == None:
                continue
            new_url = url[:pos] + injection + url[pos:]
            print("[!] Trying", new_url)

            try:
                res = s.get(new_url)
            except Exception as e:
                print(f"[!] Failed to get {new_url}: {e}")
                exit(1)
            if is_vulnerable_errors(res):
                print("[+] SQL Injection vulnerability detected, link:", new_url)
                found = True
    
    if found:
        print("INJECTION ERROR BASE FOUND FOR MYSQL")
        return

    #SQLite
    sqli_list = SQLITE_ERROR["errors"]
    for injection in sqli_list:
        new_url = f"{url}{injection}"
        print("[!] Trying", new_url)

        try:
            res = s.get(new_url)
        except Exception as e:
            print(f"[!] Failed to get {new_url}: {e}")
            exit(1)
        if is_vulnerable_errors(res):
            print("[+] SQL Injection vulnerability detected, link:", new_url)
            found = True
    if found:
        print("INJECTION ERROR BASE FOUND FOR SQLITE")
        return
    return

def parse_sql(url):
    parsed = urlparse(url)
    params = parse_qsl(parsed.query, keep_blank_values=True)
    return params

def scan_sql_injection(url):
    params = parse_sql(url)
    test_sqli_errors(url, params)

def parse_arg():
    parser = argparse.ArgumentParser(description="SQLI Scanner")
    parser.add_argument("url", help="target URL to scan")
    parser.add_argument(
        "-o",
        action="store",
        help="Archive file path, data about the scan will be saved at this path",
        default="archive.txt")
    parser.add_argument(
        "-X",
        action="store",
        help="type of http request to test, GET by default",
        default="GET")
    return parser.parse_args()

def create_session(url):
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    try:
        response = s.get(url) #init cookies
    except Exception as e:
        print(f"[!] Failed to get {url}: {e}")
        exit(1)
    #print(s.cookies.get_dict())
    return s

if __name__ == "__main__":
    url = "http://testphp.vulnweb.com/search.php?test=query"
    args = parse_arg()
    s = create_session(url)
    scan_sql_injection(url)

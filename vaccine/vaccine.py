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
        return found

    #SQLite
    sqli_list = SQLITE_ERROR["errors"]
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
         print("INJECTION ERROR BASE FOUND FOR SQLITE")
         return found
    return found

def parse_sql(url):
    parsed = urlparse(url)
    params = parse_qsl(parsed.query, keep_blank_values=True)
    return params


def find_nb_sql_args(url, params, patterns, max_test=20):

    max_found = 0
    max_param = ""
    max_pattern = ""

    for parameter, value in params:

        pos = get_insertion_position(url, parameter)
        if pos is None:
            continue

        for pattern in patterns:
            for i in range(1, max_test + 1):
                payload = pattern["payload"]
                placeholder_type = pattern["placeholder"]

                if placeholder_type == "INT":
                    replace_with = str(i)

                elif placeholder_type == "NULL_LIST":
                    replace_with = ",".join(["NULL"] * i)

                injection = payload.replace("#?#", replace_with)
                new_url = url[:pos] + injection + url[pos:]

                print("[!] trying", new_url)

                try:
                    res = s.get(new_url)
                except Exception as e:
                    print(f"[!] Failed to get {new_url}: {e}")
                    exit(1)

                if is_vulnerable_errors(res):
                    found = i - 1
                    if found > max_found:
                        max_found = found
                        max_param = parameter
                        max_pattern = payload
                    break

    return max_found, max_param, max_pattern


def test_sqli_union(url , params):
    #MySQL
    nb_column_patterns = MYSQL_ERROR["nb_column_patterns"]
    nb_args = find_nb_sql_args(url, params, nb_column_patterns);
    print(f"mysql nb args for union is: {nb_args}")
    #SQLite
    if nb_args != 0:
        return nb_args
    nb_colum_patterns = SQLITE_ERROR["nb_column_patterns"]
    nb_args = find_nb_sql_args(url, params, nb_column_patterns)
    print(f"sqlite nb args for union is : {nb_args}")


def scan_sql_injection(url):
    params = parse_sql(url)
    is_err_injectable = test_sqli_errors(url, params)
    print(f"end of err test for result {is_err_injectable}")
    if (is_err_injectable):
        #is_bool_injectable = test_sqli_boolean(url, params)
        is_union_injectable = test_sqli_union(url, params)

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
    parser.add_argument(
        "-C",
        action="store",
        help="Cookies to be send to the given URL, as Key=Value, each Key/value pair must be separated by a ';'",
        default=""
    )
    return parser.parse_args()


def create_session(url, cookies):
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    try:
        response = s.get(url) #init cookies
    except Exception as e:
        print(f"[!] Failed to get {url}: {e}")
        exit(1)
    if not cookies == "":
        print(f"Cookies={cookies}")
        pairs = cookies.split(";")
        result = {}

        for pair in pairs:
            pair = pair.strip()
            if '=' not in pair:
                raise ValueError(f"Invalid pair '{pair}': '=' not found. Cookies will be ignored")
            key, value = pair.split('=', 1)
            key = key.strip()
            value = value.strip()

            result[key] = value
        
        s.cookies.clear()
        for key, value in result.items():
            print(f"Cookies set:{key}={value}")
            s.cookies.set(key, value)
            

    return s

if __name__ == "__main__":
    args = parse_arg()
    url = args.url
    try:
        s = create_session(url, args.C)
    except Exception as e:
        print(f"Error during session creation:{e}")
    scan_sql_injection(url)

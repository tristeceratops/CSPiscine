import argparse
import ipaddress
import re
from scapy.all import get_if_list

def check_ipv4(ip:str) -> bool:
    try:
        ip_object = ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def check_mac(mac: str) -> bool:
    patterns = [
        r'^([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}$',   # xx-xx-xx-xx-xx-xx
        r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$',   # xx:xx:xx:xx:xx:xx
        r'^([0-9A-Fa-f]{3}\.){3}[0-9A-Fa-f]{3}$',  # xxx.xxx.xxx.xxx
    ]
    return any(re.fullmatch(p, mac) for p in patterns)

#--------------------argparse--------------------
parser = argparse.ArgumentParser(description="educative program about ARP poisoning")
parser.add_argument("IP-src", help="ip v4 address of the source")
parser.add_argument("MAC-src", help="MAC address of the source")
parser.add_argument("IP-target", help="ip v4 address of the target")
parser.add_argument("MAC-target", help="MAC address of the target")
args = parser.parse_args()
#--------------------checker--------------------
src = (getattr(args, "IP-src").strip(), getattr(args, "MAC-src").strip())
target = (getattr(args, "IP-target").strip(), getattr(args, "MAC-target").strip())

print(get_if_list())

if not check_ipv4(src[0]) or not check_ipv4(target[0]) or not check_mac(src[1]) or not check_mac(target[1]):
    print("Wrong format for IP or MAC address")
    exit(1)
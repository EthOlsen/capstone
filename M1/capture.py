import scapy.all as scapy

IFACENAME = 'Intel(R) Wi-Fi 6 AX201 160MHz'

def call_back(pkt):
    print(pkt, file=open('test.txt', 'a'))


capture = scapy.sniff(prn = call_back, iface=IFACENAME)

scapy.wrpcap("test.pcap", capture)
#capture.summary()

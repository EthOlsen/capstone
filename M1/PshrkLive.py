import pyshark

import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
# Dictionary to store protocol counts

protocol_counter = Counter()

def process_packet(packet):
    print(packet)
    try:
        # Extract relevant information from the packet
        protocol = packet.transport_layer
        source_ip = packet.ip.src
        destination_ip = packet.ip.dst

        # Perform your data processing or analysis here
        # For example, count the occurrence of each protocol
        protocol_counter[protocol] += 1

        # You can add more processing logic as needed

    except AttributeError as e:
        # Ignore packets that don't contain the expected attributes
        pass


def liveSniff():
    cap2 = pyshark.LiveCapture(interface='Wi-Fi', output_file='output.pcap', capture_filter='ip')
    #cap2 = pyshark.LiveCapture(interface='\\Device\\NPF_{9CCCB50F-3BE7-4573-B87B-CAF82E8E365F}', display_filter="ip")

    cap2.sniff(packet_count=15)
    
    cap2.apply_on_packets(process_packet)


    cap2.close()


liveSniff()




import pyshark
import hosts

import matplotlib.pyplot as plt

import numpy as np

FILTER = 'DNS'


cap = pyshark.FileCapture('output.pcap', display_filter=FILTER)
hostList = []
index = []
protoList = []
protoListArg = []

for packet in cap:
    try: 
        print(packet)
        pInfo = [packet.ip.src, packet.ip.dst, packet.ip.proto]
        hostList.append(pInfo)
        #destList.append(packet.ip.dst)
        #protoList.append(packet.ip.proto)
        #print(packet.ip.proto,' ',packet.ip.src,' ',packet.ip.dst,' ', packet.udp.port )
        #print(packet.highest_layer, packet[packet.highest_layer].field_names)
        #print(packet.highest_layer, packet.ip.src, packet.ip.dst, packet.ip.proto, packet.udp.srcport, packet.udp.dstport, packet.udp.payload)

    except:
        print(packet)




#for pulls protocols for pie chart
labels =[]
values = []
#vizz
for p in cap:
    x = p.transport_layer
    try:
        i = labels.index(x)
        values[i] = values[i] + 1
    except:
        labels.append(x)
        values.append(0)

#t = 0
#for p in cap:

    #if p.frame_info.time_relative < (t + 1):
    #t = t



print(labels)
print(values)
fig, ax = plt.subplots()
ax.pie(values, labels=labels)
plt.show()




#vizz

#print(list(set(destList)))
#print(cap[0].ip.src)

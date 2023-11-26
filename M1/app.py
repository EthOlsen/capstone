from flask import Flask, render_template, request
from flask_socketio import SocketIO
from scapy.all import ARP, Ether, srp
import pyshark
import asyncio
import datetime
import json


app = Flask(__name__)
socketio = SocketIO(app)

proto_counter = dict()
throughput_data = {'time': [], 'throughput': []}
dns_packets = []
top_talkers = {}
ports = []


def process_packet(packet):
    try:
        #print(packet)

        global top_talkers
        #protocol = packet.transport_layer
        protocol = packet.frame_info.protocols
        protocol = protocol.upper()
        
        selectedData = protocol.split(':')
        #selectedData.capitalize()
        protocol = ':'.join(selectedData[2:5])



        # Update protocol counts
        proto_counter[protocol] = proto_counter.get(protocol, 0) + 1
        # Emit the updated data to all connected clients
        socketio.emit('update_data', proto_counter)
        
        
        #update DNS graph
        if hasattr(packet, 'dns'):
            if(packet.dns.flags == '0x8180'):
                dns_packets.append(packet)
                str1 = f'{packet.dns.qry_name}:{packet.ip.dst}'
                socketio.emit('dnspacket', str1)


        #updates for time line graph
        time = packet.sniff_timestamp
        throughput_value = packet.captured_length
        throughput_data['time'].append(time)
        throughput_data['throughput'].append(throughput_value)
        
        # Send the throughput data to all connected clients
        socketio.emit('update_throughput', throughput_data)
        
        try:
            source_ip = packet.ip.src
            destination_ip = packet.ip.dst
            top_talkers[source_ip] = top_talkers.get(source_ip, 0) + 1

            if hasattr(packet, 'tcp'):
                    portString = f"{source_ip}:{packet.tcp.srcport}"

                    if portString not in ports:
                        ports.append(portString)
                

                #print(packet.tcp.srcport + ' -- ' + packet.tcp.dstport)
            #if hasattr(packet, 'udp'):
                #ports.append(packet.tcp.srcport + ' --> ' + packet.tcp.dstport)
                #print(packet.udp.srcport + ' -- ' + packet.udp.dstport)
        # Send updates to the client
            socketio.emit('update_top_talkers', {
            'topTalkers': top_talkers,
            'ports': ports
        })
            
        except:
            pass
        #topTalkers

        # Update top_talkers dictionary with source IP as the key


        


    except AttributeError as e:
        # Ignore packets that don't contain the expected attributes
        print("attribute error")
        print(packet)
        pass



def live_sniff():
    global top_talkers
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    cap = pyshark.LiveCapture(interface='Wi-Fi',output_file='liveCaptureOutput.pcap')
    for packet in cap.sniff_continuously(packet_count=10000):  # Adjust packet_count as needed
        try:
            process_packet(packet)
        except Exception as e:
            print(f"Error processing packet: {e}")

    loop.run_until_complete(asyncio.gather())

@socketio.on('get_arp_results')
def get_arp_results():
    print('get arp results')
    target_ip = "192.168.1.1/24"
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=0)[0]
    clients = []

    for sent, received in result:
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})

    socketio.emit('arp_results', {'clients': clients})


# Home route
@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message_from_client')
def handle_message(message):
    print('Message from client:', message)
    socketio.emit('message_from_server', message)
@app.route('/images/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


if __name__ == '__main__':

    socketio.start_background_task(live_sniff)
    socketio.run(app, debug=True)

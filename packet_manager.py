from scapy.sendrecv import sniff
from scapy.utils import wrpcap, rdpcap


def capture_packets(interface, ip, packet_count, output_file):
    print("Starting Capture...")
    capture = sniff(iface=interface, filter=f"host {ip}",
                    count=packet_count)
    print("Capture completed...")
    wrpcap(output_file, capture)
    print("File saved as " + output_file)


def read_packets(file_name):
    print("Below is the captured packet summary:")
    packets = rdpcap(file_name)
    print(packets.summary())

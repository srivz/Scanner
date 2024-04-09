from scapy.sendrecv import sniff
from scapy.utils import wrpcap


def capture_with_scapy(interface, source_ip, destination_ip, packet_count, output_file):
    capture = sniff(iface=interface, filter=f"ip.addr == {source_ip} and ip.addr == {destination_ip}",
                    count=packet_count)
    wrpcap(output_file, capture)


# Example usage
if __name__ == "__main__":
    interface = "Local Area Connection* 2"  # Example interface name
    source_ip = "192.168.137.63"  # Example source IP address
    destination_ip = "192.168.137.63"  # Example destination IP address
    packet_count = 10  # Example number of packets to capture
    output_file = "captured_packets/file" + source_ip.replace(".", "_") + ".pcap"

    capture_with_scapy(interface, source_ip, destination_ip, packet_count, output_file)

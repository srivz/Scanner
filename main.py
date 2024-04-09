import os
import time
import socket

from arp_scanner import arp_scan, get_mac_address
from network_interfaces import get_network_interfaces_psutil, get_network_details, calculate_network_range
from packet_manager import capture_packets, read_packets
from wifi_connecter import connect_to_wifi
from wifi_scanner import list_available_wifi_networks

available_networks = list_available_wifi_networks()
if available_networks:
    print("Available Wi-Fi networks:")
    for network in available_networks:
        print(network)
else:
    print("No Wi-Fi networks found.")
print("\n")
print("Do you want to connect to a different Network? (y) or (n)")
choice = input()
connected = False
if choice.lower() == 'y':
    ssid = input("Enter the SSID to connect: ")
    connected = connect_to_wifi(ssid)
elif choice.lower() == 'n':
    connected = True
else:
    connected = True
if connected:
    interfaces = get_network_interfaces_psutil()
    wireless_interfaces = {}
    for interface, addresses in interfaces.items():
        for address in addresses:
            if address.family == socket.AF_INET:
                wireless_interfaces[interface] = address.address

    if wireless_interfaces:
        print("Available wireless interfaces:")
        for idx, (interface, ip_address) in enumerate(wireless_interfaces.items(), start=1):
            print(f"{idx}. {interface}: {ip_address}")

        selection = input("Select a wireless interface (enter the corresponding number): ")
        try:
            selection = int(selection)
            if 1 <= selection <= len(wireless_interfaces):
                selected_interface = list(wireless_interfaces.keys())[selection - 1]
                print(f"Selected wireless interface: {selected_interface}")
                ip_address, subnet_mask = get_network_details(selected_interface)
                if ip_address and subnet_mask:
                    print(f"Detected IP Address: {ip_address}")
                    print(f"Detected Subnet Mask: {subnet_mask}")
                    network_range = calculate_network_range(ip_address, subnet_mask)
                    print(f"Calculated Network Range: {network_range}")
                    active_devices = arp_scan(selected_interface, network_range)
                    print(active_devices)
                    ip = input("Enter ip to capture packets:")
                    mac = get_mac_address(ip, active_devices)
                    packet_count = int(input("Enter number of packets to capture:"))
                    output_file = "captured_packets/file-" + ip.replace(".", "_") + "-" + str(mac).replace(":",
                                                                                                           "_") + "-" + str(
                        time.time()).replace(".", "_") + ".pcap"
                    output_dir = os.path.dirname(output_file)
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    capture_packets(selected_interface, ip, packet_count, output_file)
                    read_packets(output_file)
                else:
                    print("Failed to detect IP address and subnet mask.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        print("No wireless interfaces found.")

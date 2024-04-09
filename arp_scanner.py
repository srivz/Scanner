from scapy.all import ARP, Ether, srp
from prettytable import PrettyTable

from mac_address_lookup import query_mac_address_lookup


def arp_scan(network_interface, net_range):
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=net_range)
    result = srp(arp_request, timeout=3, iface=network_interface, verbose=False)[0]
    devices = []
    for sent, received in result:
        devices.append({'IP': received.psrc, 'MAC Address': received.hwsrc,
                        'Manufacturer info': query_mac_address_lookup(received.hwsrc)})
    table = PrettyTable()
    table.field_names = devices[0].keys()
    for device in devices:
        table.add_row(device.values())
    print(table)
    return devices


def get_mac_address(ip_address, device_list):
    for device in device_list:
        if device['IP'] == ip_address:
            return device['MAC Address']
    return None

import subprocess


def list_available_wifi_networks():
    try:
        # Execute 'netsh wlan show networks' command to get available Wi-Fi networks
        result = subprocess.run(['netsh', 'wlan', 'show', 'network'], capture_output=True, text=True)

        # Check if the command executed successfully
        if result.returncode == 0:
            # Extract SSIDs from the command output
            networks = [line.split(':')[1].strip() for line in result.stdout.split('\n') if 'SSID' in line]
            return networks
        else:
            print("Error: Failed to execute 'netsh wlan show networks' command.")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# def get_device_info(ip_addr):
#     try:
#         nm = nmap.PortScanner()
#         nm.scan(hosts=ip_addr, arguments='-O')  # Perform OS detection
#         device_info = nm[ip_addr]
#
#         # Extract device details
#         device_name = device_info['hostnames'][0]['name'] if 'hostnames' in device_info else 'Unknown'
#         manufacturer = device_info['vendor'][device_info['addresses']['mac']]
#         device_type = device_info['osmatch'][0]['osclass'][0]['type'] if 'osmatch' in device_info else 'Unknown'
#
#         return {'ip': ip_addr, 'name': device_name, 'mac': device_info['addresses']['mac'],
#                 'manufacturer': manufacturer, 'device_type': device_type}
#     except Exception as e:
#         print(f"Error getting device info for {ip_addr}: {e}")
#         return None

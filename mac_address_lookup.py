
import requests
def query_mac_address_lookup(mac_address):
    oui = mac_address[:8].replace(':', '')
    url = f"https://api.macvendors.com/{oui}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Unknown"
    except Exception as e:
        print(f"Error querying MAC address lookup service: {e}")
        return "Unknown"

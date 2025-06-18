import scapy.all as scapy
import requests
import socket
# import re
import sys 

# --- Configuration ---
# Таймаут для ARP-запросов Scapy
SCAPY_ARP_TIMEOUT = 10 
# Таймаут для HTTP-запросов к API вендоров MAC
REQUESTS_TIMEOUT = 10
# URL для получения информации о вендорах MAC-адресов
MACVENDORS_API_URL = "https://api.macvendors.com/"

def scan_network(ip_range):
    """
    Сканирует локальную сеть для обнаружения активных устройств с использованием ARP-запросов.

    Args:
        ip_range (str): Диапазон IP-адресов для сканирования (например, "192.168.1.1/24").

    Returns:
        list: Список словарей, где каждый словарь содержит 'ip' и 'mac' обнаруженного устройства.
    """
    try:
        # Создаем ARP-запрос для заданного диапазона IP
        arp_request = scapy.ARP(pdst=ip_range)
        # Создаем широковещательный Ethernet-фрейм
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        # Объединяем Ethernet-фрейм и ARP-запрос
        packet = broadcast / arp_request
        # Отправляем пакет и получаем ответы. verbose=False отключает вывод Scapy.
        answered, unanswered = scapy.srp(packet, timeout=SCAPY_ARP_TIMEOUT, verbose=False)
    except Exception as e:
        print(f"Ошибка при сканировании сети: {e}")
        # Завершаем выполнение программы, так как сканирование является критическим шагом
        sys.exit(1) 

    devices = []
    # Извлекаем IP и MAC-адреса из полученных ответов
    for element in answered:
        devices.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
    return devices

def get_mac_vendor(mac_address):
    """
    Получает название вендора по MAC-адресу, используя внешний API.

    Args:
        mac_address (str): MAC-адрес устройства.

    Returns:
        str: Название вендора или "Неизвестный вендор", если информация не найдена или произошла ошибка.
    """
    try:
        response = requests.get(f"{MACVENDORS_API_URL}{mac_address}", timeout=REQUESTS_TIMEOUT)
        response.raise_for_status()  # Вызовет исключение для кодов состояния HTTP 4xx/5xx
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        # print(f"Не удалось получить вендора для MAC {mac_address}: {e}") # Отладочный вывод
        return "Неизвестный вендор"

def get_device_hostname(ip_address):
    """
    Пытается получить имя хоста по IP-адресу.

    Args:
        ip_address (str): IP-адрес устройства.

    Returns:
        str: Имя хоста или None, если имя хоста не может быть разрешено.
    """
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname
    except socket.herror:
        return None
    except socket.timeout:
        return None
    except Exception as e:
        # print(f"Ошибка при получении имени хоста для IP {ip_address}: {e}") # Отладочный вывод
        return None

def determine_device_type(vendor_name, hostname=None, mac_address=None):
    """
    Пытается угадать тип устройства на основе информации о вендоре, имени хоста и MAC-адресе.
    Правила упорядочены от более специфичных к более общим.

    Args:
        vendor_name (str): Название вендора.
        hostname (str, optional): Имя хоста. Defaults to None.
        mac_address (str, optional): MAC-адрес. Defaults to None.

    Returns:
        str: Предполагаемый тип устройства.
    """
    vendor_lower = (vendor_name or "").lower()
    hostname_lower = (hostname or "").lower()
    mac_lower = (mac_address or "").lower()

    # --- Правила на основе имени хоста (часто очень точные) ---
    if any(x in hostname_lower for x in ["iphone", "ipad", "ios"]):
        return "Смартфон / Планшет (iOS)"
    if any(x in hostname_lower for x in ["android", "phone", "tablet", "sm-", "gt-"]): # sm- и gt- частые префиксы моделей Samsung
        return "Смартфон / Планшет (Android)"
    if "apple-tv" in hostname_lower or "appletv" in hostname_lower:
        return "Apple TV"
    if any(x in hostname_lower for x in ["desktop", "laptop", "pc", "windows", "linux", "macbook", "host", "srv", "workstation"]):
        return "ПК / Ноутбук"
    if any(x in hostname_lower for x in ["docker", "kube", "vmware", "virtualbox", "proxmox", "hyper-v"]):
        return "Виртуальная машина / Контейнер / Гипервизор"
    if any(x in hostname_lower for x in ["printer", "hp", "canon", "epson", "xerox", "brother"]):
        return "Принтер / МФУ"
    if any(x in hostname_lower for x in ["router", "gateway", "modem", "accesspoint", "ap", "wifi"]):
        return "Маршрутизатор / Точка доступа / Модем"
    if any(x in hostname_lower for x in ["switch", "managedswitch"]):
        return "Сетевой коммутатор"
    if any(x in hostname_lower for x in ["nvr", "dvr", "ipcam", "camera"]):
        return "Камера видеонаблюдения / NVR/DVR"
    if any(x in hostname_lower for x in ["tv", "smarttv", "roku", "chromecast", "firetv", "webos", "tizen"]):
        return "Смарт ТВ / Медиаплеер"
    if any(x in hostname_lower for x in ["esp", "arduino", "micropython", "iot"]):
        return "IoT-устройство / Микроконтроллер"
    if "raspberrypi" in hostname_lower or "rpi" in hostname_lower:
        return "Raspberry Pi"
    if any(x in hostname_lower for x in ["nas", "synology", "qnap", "truenas"]):
        return "Сетевое хранилище (NAS)"
    if "xbox" in hostname_lower or "playstation" in hostname_lower or "nintendo" in hostname_lower:
        return "Игровая консоль"

    # --- Правила на основе вендора (после имени хоста, так как имя хоста часто точнее) ---
    if "apple" in vendor_lower:
        return "Смартфон / Mac / Apple Watch"
    elif "samsung" in vendor_lower:
        return "Смартфон / ТВ / Умный дом Samsung"
    elif "lg" in vendor_lower:
        return "Смарт ТВ / Бытовая техника LG"
    elif "intel" in vendor_lower or "amd" in vendor_lower:
        return "ПК / Ноутбук (Процессор Intel/AMD)"
    elif any(x in vendor_lower for x in ["microsoft", "hp", "dell", "lenovo", "asus", "acer", "msi", "gigabyte", "fujitsu"]):
        return "ПК / Ноутбук"
    elif any(x in vendor_lower for x in ["huawei", "xiaomi", "oneplus", "oppo", "vivo"]):
        return "Смартфон / Планшет (Китайские бренды)"
    elif any(x in vendor_lower for x in ["tp-link", "cisco", "netgear", "d-link", "ubiquiti", "mikrotik", "linksys", "asuscomm", "zte", "keenetic"]):
        return "Маршрутизатор / Сетевое устройство"
    elif "amazon" in vendor_lower:
        return "Устройство Amazon (Echo, Fire TV, Kindle)"
    elif "google" in vendor_lower:
        return "Устройство Google (Chromecast, Pixel, Nest)"
    elif "sony" in vendor_lower:
        return "Телевизор / Игровая консоль Sony"
    elif "panasonic" in vendor_lower:
        return "Телевизор / Камера Panasonic"
    elif "philips" in vendor_lower:
        return "Смарт ТВ / Умный свет Philips Hue"
    elif "hichip" in vendor_lower or "hikvision" in vendor_lower or "dahua" in vendor_lower:
        return "Камера видеонаблюдения"
    elif "tenda" in vendor_lower or "mercury" in vendor_lower or "comfast" in vendor_lower:
        return "Сетевое устройство (бюджетные бренды)"
    elif "grandstream" in vendor_lower or "yealink" in vendor_lower:
        return "VoIP-телефон / Коммуникационное оборудование"
    elif "insteon" in vendor_lower or "zigbee" in vendor_lower or "z-wave" in vendor_lower: # Это не вендоры, но могут быть в названии
        return "Умный дом / IoT-хаб"
    elif "hon hai" in vendor_lower or "fugui" in vendor_lower or "compal" in vendor_lower or "quanta" in vendor_lower:
        return "Производитель OEM (ПК / Ноутбук)" # Это крупные производители для многих брендов

    # --- Правила на основе MAC-адреса (если вендор и хост не дали результатов) ---
    # MAC-адреса, начинающиеся с 02: или 0A:, часто указывают на локально администрируемые адреса
    # или виртуальные машины.
    
    if mac_lower.startswith("02:") or mac_lower.startswith("0a:") or mac_lower.startswith("00:50:56:"): # VMware
        return "Виртуальная машина / Контейнер"
    
    # Можно добавить другие известные префиксы MAC для специфичных устройств, если известны.
    # Например:
    if mac_lower.startswith("b8:27:eb"): # Raspberry Pi Foundation
       return "Raspberry" 

    if vendor_lower == "неизвестный вендор":
    # Если имя хоста содержит "mobile", "phone", "celular", то это мобильное
        if any(x in hostname_lower for x in ["mobile", "phone", "celular"]):
            return "Мобильное устройство (Неизвестный вендор)"
        return "Неизвестное устройство"

def main():
    """
    Основная функция для запуска сканирования сети и отображения результатов.
    """
    print("--- Инструмент сканирования сети ---")
    ip_range = input("Введите диапазон сети (например, 192.168.1.1/24): ")

    print(f"\nСканирование вашей сети ({ip_range})...\n")
    devices = scan_network(ip_range)

    if not devices:
        print("Активных устройств в указанном диапазоне не найдено.")
        return

    print("Обнаруженные устройства:")
    print("-" * 100)
    print(f"{'IP-адрес':<18} {'MAC-адрес':<19} {'Вендор':<28} {'Имя хоста':<22} {'Тип устройства'}")
    print("-" * 100)

    for device in devices:
        vendor = get_mac_vendor(device['mac'])
        hostname = get_device_hostname(device['ip'])
        device_type = determine_device_type(vendor, hostname, device['mac']) 
        
        print(f"{device['ip']:<18} {device['mac']:<19} {vendor:<28} {hostname or 'Н/Д':<22} {device_type}")
    
    print("-" * 100)
    print("\nСканирование завершено.")

if __name__ == "__main__":
    main()
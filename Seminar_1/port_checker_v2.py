import socket

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        result = s.connect_ex((host, port))
        return result == 0

def main():
    host = '127.0.0.1'
    ports = range(8000, 10_000)
    open_ports = []

    print(f"Проверка портов на {host}...\n")
    for port in ports:
        if check_port(host, port):
            print(f"Порт {port}: ОТКРЫТ")
            open_ports.append(port)
        else:
            print(f"Порт {port}: закрыт")

    print("\nРезультат:")
    if open_ports:
        print("Открытые порты:")
        for port in open_ports:
            print(f" - {port}")
    else:
        print("❌ Все порты в указанном диапазоне закрыты.")

if __name__ == "__main__":
    main()

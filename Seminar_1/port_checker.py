# python -m http.server 9000

import socket

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)  # Пауза в полсекунды
        result = s.connect_ex((host, port))
        return result == 0

def main():
    host = '127.0.0.1'  # Локальная машина
    ports = [8000, 8080, 8888, 9000, 1880, 3000] # Добавьте любые интересующие порты
    # ports = range(8000,10_000)

    print(f"Проверка портов на {host}...\n")
    for port in ports:
        status = "ОТКРЫТ" if check_port(host, port) else "закрыт"
        print(f"Порт {port}: {status}")

if __name__ == "__main__":
    main()

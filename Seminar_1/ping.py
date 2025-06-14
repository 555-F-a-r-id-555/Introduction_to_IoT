import dns.resolver
import time

# Список DNS-серверов
dns_servers = [
    "217.64.23.170",
    "81.17.90.248",
    "81.17.89.73",
    "81.17.81.34",
    "81.17.93.146",
    "81.17.94.238",
    "216.146.35.35",
    "216.146.35.36",
]


test_domain = "google.com"

print("Тест производительности DNS-серверов:\n")

for ip in dns_servers:
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [ip]
    resolver.lifetime = 3  # Таймаут в секундах

    try:
        start = time.time()
        answer = resolver.resolve(test_domain)
        end = time.time()
        ms = round((end - start) * 1000, 2)

        print(f"[✔] {ip} — ответ за {ms} мс → {answer[0]}")
    except Exception as e:
        print(f"[✘] {ip} — не отвечает: {str(e).split(':')[0]}")


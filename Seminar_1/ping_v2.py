import dns.resolver
import time


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
attempts = 3

results = []

print(f"Тест производительности DNS-серверов (домен: {test_domain}, попыток: {attempts})\n")

for ip in dns_servers:
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [ip]
    resolver.lifetime = 3

    times = []
    success = False
    ip_response = None

    for i in range(attempts):
        try:
            start = time.time()
            answer = resolver.resolve(test_domain)
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
            success = True
            if not ip_response:
                ip_response = str(answer[0])
        except Exception:
            pass

    if success and times:
        avg_time = round(sum(times) / len(times), 2)
        results.append((ip, avg_time, ip_response))
    else:
        results.append((ip, None, None))

# Сортируем по среднему времени ответа (если есть)
results.sort(key=lambda x: float('inf') if x[1] is None else x[1])


for ip, avg_time, ip_response in results:
    if avg_time is not None:
        print(f"[✔] {ip} — среднее время: {avg_time} мс → {ip_response}")
    else:
        print(f"[✘] {ip} — не отвечает")

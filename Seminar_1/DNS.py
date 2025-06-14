# pip install dnspython
import dns.resolver
import json

dns_list = [
    {"ip": "217.64.23.170", "city": "Baku"},
    {"ip": "81.17.90.248", "city": "Baku"},
    {"ip": "81.17.89.73", "city": "Baku"},
    {"ip": "81.17.81.34", "city": "Baku"},
    {"ip": "81.17.93.146", "city": "Baku"},
    {"ip": "81.17.94.238", "city": "Baku"},
    {"ip": "216.146.35.35", "city": "Baku"},
    {"ip": "216.146.35.36", "city": "Baku"},
]

for dns_entry in dns_list:
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_entry["ip"]]
    try:
        answer = resolver.resolve("google.com", lifetime=3)
        print(f"[✔] {dns_entry['ip']} — работает, ответ: {answer[0]}")
    except Exception as e:
        print(f"[✘] {dns_entry['ip']} — не отвечает: {e}")

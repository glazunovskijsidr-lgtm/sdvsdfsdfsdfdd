import requests
import random
import time
import os

sym = "abcdefghijklmnopqrstuvwxyz"

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    banner = """
░█████╗░██╗░░░██╗████████╗░█████╗░░░░░░░██████╗░███████╗░██████╗░
██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗░░░░░░██╔══██╗██╔════╝██╔════╝░
███████║██║░░░██║░░░██║░░░██║░░██║█████╗██████╔╝█████╗░░██║░░██╗░
██╔══██║██║░░░██║░░░██║░░░██║░░██║╚════╝██╔══██╗██╔══╝░░██║░░╚██╗
██║░░██║╚██████╔╝░░░██║░░░╚█████╔╝░░░░░░██║░░██║███████╗╚██████╔╝
╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░░╚════╝░░░░░░░╚═╝░░╚═╝╚══════╝░╚═════╝░

███╗░░░███╗░█████╗░██╗██╗░░░░░░░░████████╗███╗░░░███╗
████╗░████║██╔══██╗██║██║░░░░░░░░╚══██╔══╝████╗░████║
██╔████╔██║███████║██║██║░░░░░░░░░░░██║░░░██╔████╔██║
██║╚██╔╝██║██╔══██║██║██║░░░░░░░░░░░██║░░░██║╚██╔╝██║
██║░╚═╝░██║██║░░██║██║███████╗██╗░░░██║░░░██║░╚═╝░██║
╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝╚══════╝╚═╝░░░╚═╝░░░╚═╝░░░░░╚═╝
"""
    print(banner)

def convert_accounts_format():
    if not os.path.exists("accounts.txt"):
        print("[❌] Файл accounts.txt не найден!")
        return

    with open("accounts.txt", "r", encoding="utf-8") as f:
        accounts = [line.strip() for line in f if ":" in line]

    if not accounts:
        print("[❌] В accounts.txt нет аккаунтов для преобразования!")
        return

    formatted_accounts = []

    for account in accounts:
        email, password = account.split(":")
        formatted_accounts.append(f"Mail: {email}\nPassword: {password}\n\n")

    with open("accounts_format.txt", "w", encoding="utf-8") as f:
        f.writelines(formatted_accounts)

    print(f"\n✅ Преобразование завершено! Сохранено {len(accounts)} аккаунтов в accounts_format.txt.")
    input("\nНажмите Enter, чтобы вернуться в меню...")

def check_accounts():
    if not os.path.exists("accounts.txt"):
        print("[❌] Файл accounts.txt не найден!")
        return

    with open("accounts.txt", "r", encoding="utf-8") as f:
        # Пропускаем первые 4 строки (3 текста и пустая строка)
        accounts = [line.strip() for line in f.readlines()[4:] if ":" in line]

    if not accounts:
        print("[❌] В accounts.txt нет аккаунтов для проверки!")
        return

    valid_accounts = []
    invalid_accounts = []

    print(f"\n🔍 Начинаем проверку {len(accounts)} аккаунтов...\n")

    for index, account in enumerate(accounts, start=1):
        email, password = account.split(":")
        print(f"[{index}/{len(accounts)}] Проверка: {email}")

        try:
            response = requests.post(
                "https://api.mail.tm/token",
                json={"address": email, "password": password},
                timeout=10
            )

            if response.status_code == 200:
                print(f"[✅] Валидный аккаунт: {email}")
                valid_accounts.append(account)
            else:
                print(f"[❌] Невалидный аккаунт: {email}")
                invalid_accounts.append(account)

        except requests.exceptions.RequestException as e:
            print(f"[⚠] Ошибка соединения: {e}. Ожидание 30 секунд...")
            time.sleep(30)
            invalid_accounts.append(account)

        time.sleep(5)

    with open("valid.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(valid_accounts) + "\n")

    with open("invalid.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(invalid_accounts) + "\n")

    print("\n✅ Проверка завершена!")
    print(f"✔ Рабочие аккаунты: {len(valid_accounts)}")
    print(f"❌ Нерабочие аккаунты: {len(invalid_accounts)}")

    input("\nНажмите Enter, чтобы вернуться в меню...")

def register_account_v1():
    clear_console()
    print_banner()

    try:
        domain = requests.get("https://api.mail.tm/domains", timeout=10).json()["hydra:member"][0]["domain"]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка получения домена: {e}")
        return

    failed_attempts = 0

    while True:
        login = "".join(random.choice(sym) for _ in range(random.randint(7, 13)))
        password = "".join(random.choice(sym) for _ in range(random.randint(7, 13)))

        try:
            response = requests.post(
                "https://api.mail.tm/accounts",
                json={"address": f"{login}@{domain}", "password": password},
                timeout=10
            )

            if response.status_code == 201:
                with open("accounts.txt", "a", encoding="utf-8") as f:
                    if os.path.getsize("accounts.txt") == 0:
                        f.write("Аккаунты были зарегистрированы auto-reg.\n")  # Первая строка с текстом
                        f.write("Вход в аккаунты тут  → → → https://mail.tm/ru/\n")  # Вторая строка с текстом
                        f.write("Список аккаунтов:\n\n")  # Третья строка с текстом
                    f.write(f"{login}@{domain}:{password}\n")
                print(f"[✅] Аккаунт зарегистрирован: {login}@{domain}")
                failed_attempts = 0  # сбрасываем счетчик после успешной регистрации

            elif response.status_code == 429:
                print("[❌] Ошибка 429 (слишком много запросов). Ждем 60 секунд и пробуем снова...")
                time.sleep(60)
                failed_attempts += 1

            elif response.status_code == 500:
                print("[❌] Ошибка 500 (внутренняя ошибка сервера). Ждем 30 секунд и пробуем снова...")
                time.sleep(30)
                failed_attempts += 1

            else:
                print(f"[❌] Ошибка: {response.status_code}, пропускаем аккаунт.")
                failed_attempts += 1

            if failed_attempts >= 3:
                print("[❌] Достигнут лимит попыток с ошибкой 500 или 429. Прекращаем создание аккаунтов.")
                break

        except requests.exceptions.RequestException as e:
            print(f"[⚠️] Ошибка соединения: {e}. Ждем 30 секунд...")
            time.sleep(30)
            failed_attempts += 1

        print(f"[⏳] Ожидание {random.randint(10, 20)} секунд перед следующим аккаунтом...")
        time.sleep(random.randint(10, 20))

    input("\n✅ Создание аккаунтов завершено! Нажмите Enter, чтобы вернуться в меню...")

def register_account_v2():
    clear_console()
    print_banner()

    try:
        num_accounts = int(input("Сколько аккаунтов создать?: "))
        delay = int(input("Введите задержку между регистрациями (в секундах): "))
    except ValueError:
        print("[❌] Ошибка: Введите число!")
        time.sleep(2)
        return

    if not os.path.exists("accounts.txt"):
        with open("accounts.txt", "w", encoding="utf-8") as f:
            f.write("Список зарегистрированных аккаунтов:\n\n")

    try:
        domain = requests.get("https://api.mail.tm/domains", timeout=10).json()["hydra:member"][0]["domain"]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка получения домена: {e}")
        return

    failed_attempts = 0

    for i in range(1, num_accounts + 1):
        login = "".join(random.choice(sym) for _ in range(random.randint(7, 13)))
        password = "".join(random.choice(sym) for _ in range(random.randint(7, 13)))

        try:
            response = requests.post(
                "https://api.mail.tm/accounts",
                json={"address": f"{login}@{domain}", "password": password},
                timeout=10
            )

            if response.status_code == 201:
                with open("accounts.txt", "a", encoding="utf-8") as f:
                    if os.path.getsize("accounts.txt") == 0:
                        f.write("Текст 1\n\n")  # Первая строка с текстом
                        f.write("Текст 2\n\n")  # Вторая строка с текстом
                        f.write("Текст 3\n\n")  # Третья строка с текстом
                    f.write(f"{login}@{domain}:{password}\n")
                print(f"[✅] [{i}/{num_accounts}] Аккаунт зарегистрирован: {login}@{domain}")
                failed_attempts = 0

            elif response.status_code == 429:
                print("[❌] Ошибка 429 (слишком много запросов). Ждем 60 секунд и пробуем снова...")
                time.sleep(60)
                failed_attempts += 1

            elif response.status_code == 500:
                print("[❌] Ошибка 500 (внутренняя ошибка сервера). Ждем 30 секунд и пробуем снова...")
                time.sleep(30)
                failed_attempts += 1

            else:
                print(f"[❌] Ошибка: {response.status_code}, пропускаем аккаунт.")
                failed_attempts += 1

            if failed_attempts >= 3:
                print("[❌] Достигнут лимит попыток с ошибкой 500 или 429. Прекращаем создание аккаунтов.")
                break

        except requests.exceptions.RequestException as e:
            print(f"[⚠] Ошибка соединения: {e}. Ждем 30 секунд...")
            time.sleep(30)
            failed_attempts += 1

        if i < num_accounts:
            print(f"[⏳] Ожидание {delay} секунд перед следующим аккаунтом...")
            time.sleep(delay)

    input("\n✅ Создание аккаунтов завершено! Нажмите Enter, чтобы вернуться в меню...")

def print_dots_animation():
    print("Запуск авторега", end="")
    for _ in range(3):  
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()

def main():
    while True:
        clear_console()
        print_banner()
        print("\n1. Мои аккаунты")
        print("2. Создать аккаунты")
        print("3. Проверить аккаунты")  
        print("4. Преобразовать аккаунты")  
        print("5. Выйти")  
        choice = input("Выберите действие: ")

        if choice == "1":
            os.system("notepad accounts.txt" if os.name == "nt" else "nano accounts.txt")
            clear_console()  
            print_banner()  
            continue  
        elif choice == "2":
            clear_console()  
            print_banner()  
            print("\n1. Автоматический (V1)")
            print("2. Настраеваемый (V2)")
            print("3. Назад")
            sub_choice = input("Выберите версию: ")

            if sub_choice == "1":
                clear_console()
                print_banner()
                print_dots_animation()  
                time.sleep(5)  
                print("Выбран режим: Автоматическйи (V1)")
                print("Запускаем авторег...")
                register_account_v1()  
            elif sub_choice == "2":
                clear_console()
                print_banner()
                print_dots_animation()  
                time.sleep(5)  
                print("Выбран режим: Настраеваемый (V2)")
                print("Запускаем авторег...")
                register_account_v2()  
            elif sub_choice == "3":
                continue  
        elif choice == "3":  
            clear_console()
            print_banner()
            check_accounts()
        elif choice == "4":  
            clear_console()
            print_banner()
            convert_accounts_format()
        elif choice == "5":  
            print("[✅] Выход из программы...")
            time.sleep(2)
            break  
        else:
            print("[❌] Неверный ввод!")

if __name__ == "__main__":
    main()

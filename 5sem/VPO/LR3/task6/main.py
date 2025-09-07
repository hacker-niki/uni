import requests
import os
import sys

def download_file(url, save_dir):
    try:
        # Получаем имя файла из URL
        file_name = 'filename'
        file_path = os.path.join(save_dir, file_name)

        # Проверяем, существует ли директория
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Загружаем файл
        response = requests.get(url)
        response.raise_for_status()

        # Сохраняем файл
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"Файл успешно сохранён: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при загрузке: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <URL> <путь_к_папке>")
    else:
        url = sys.argv[1]
        save_dir = sys.argv[2]
        download_file(url, save_dir)
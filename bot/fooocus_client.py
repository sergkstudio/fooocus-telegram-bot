import requests
import os

# URL для API Fooocus, заданный через переменные окружения
FOOCUS_URL = os.getenv("FOOCUS_URL")

def generate_image_with_fooocus(prompt):
    """
    Отправляет запрос к API Fooocus для генерации изображения по описанию.
    """
    try:
        # Параметры запроса
        payload = {
            "prompt": prompt
        }

        # Отправка POST-запроса к API
        response = requests.post(f"{FOOCUS_URL}/generate", json=payload)
        response.raise_for_status()

        # Проверка и обработка ответа
        if response.status_code == 200:
            result = response.json()
            image_url = result.get("image_url")  # Или другой ключ, если формат отличается
            return image_url
        else:
            print(f"Ошибка: код {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении к API: {e}")
        return None

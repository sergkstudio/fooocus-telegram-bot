# Fooocus Telegram Bot

Телеграм бот для генерации изображений через Fooocus API.

## Требования

- Python 3.10 или выше
- Docker (опционально)
- Доступ к Fooocus API (должен быть запущен и доступен по указанному URL)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/fooocus-telegram-bot.git
cd fooocus-telegram-bot
```

2. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

3. Отредактируйте `.env` файл, добавив ваш токен Telegram бота и URL Fooocus API.

## Запуск

### Без Docker

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите бота:
```bash
python bot.py
```

### С Docker

1. Соберите Docker образ:
```bash
docker build -t fooocus-telegram-bot .
```

2. Запустите контейнер:
```bash
docker run -d --env-file .env --name fooocus-bot fooocus-telegram-bot
```

## Использование

1. Найдите вашего бота в Telegram
2. Отправьте команду `/start` для начала работы
3. Отправьте текстовый промпт для генерации изображения
4. Дождитесь результата

## Примечания

- Убедитесь, что Fooocus API доступен по указанному URL
- Для работы бота необходим валидный токен Telegram бота
- Время генерации изображения может варьироваться в зависимости от нагрузки на API 
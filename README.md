# Fooocus Telegram Bot

Телеграм бот для генерации изображений с помощью Fooocus API.

## Установка

### Локальный запуск

1. Клонируйте репозиторий
2. Установите зависимости:
```bash
pip install -r requirements.txt
```

### Запуск в Docker

1. Убедитесь, что у вас установлены Docker и Docker Compose
2. Создайте файл `.env` с необходимыми переменными окружения:
```bash
TELEGRAM_TOKEN=your_telegram_bot_token_here
FOOOCUS_API_URL=http://your-fooocus-api-url:8188
```
3. Соберите и запустите контейнер:
```bash
docker-compose up -d
```

## Настройка

1. Создайте бота в Telegram через [@BotFather](https://t.me/botfather)
2. Получите токен бота
3. Отредактируйте файл `.env`:
   - Замените `your_telegram_bot_token_here` на ваш токен бота
   - При необходимости измените URL API Fooocus

## Использование

1. Отправьте команду `/start` для начала работы
2. Отправьте текстовое описание того, что вы хотите увидеть
3. Бот сгенерирует изображение и отправит его в чат

## Управление Docker контейнером

- Запуск бота:
```bash
docker-compose up -d
```

- Остановка бота:
```bash
docker-compose down
```

- Просмотр логов:
```bash
docker-compose logs -f
```

## Требования

- Python 3.7+ (для локального запуска)
- Docker и Docker Compose (для запуска в контейнере)
- Доступ к API Fooocus
- Токен Telegram бота 
# Dockerfile для Telegram-бота и сервера

# Используем базовый образ для Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY bot/requirements.txt /app/bot/requirements.txt
COPY server/requirements.txt /app/server/requirements.txt
RUN pip install -r bot/requirements.txt && pip install -r server/requirements.txt

# Копируем код бота и сервера
COPY bot /app/bot
COPY server /app/server

# Команда запускает сервер и бота
CMD ["sh", "-c", "python3 /app/server/server.py & python3 /app/bot/bot.py"]
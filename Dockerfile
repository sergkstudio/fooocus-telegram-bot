FROM python:3.10-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

# Копирование файлов проекта
COPY . .

# Запуск бота
CMD ["python", "bot.py"] 
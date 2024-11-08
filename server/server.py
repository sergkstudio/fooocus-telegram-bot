from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler
import os
import requests

app = Flask(__name__)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

# Функция для генерации изображения
def generate_image(prompt):
    api_url = "https://sd.klepinin.space/api/generate"  # Замените на актуальный эндпоинт из документации
    payload = {
        "prompt": prompt,
        "steps": 50,  # Задайте нужные параметры, исходя из документации
        "width": 512,
        "height": 512,
    }
    response = requests.post(api_url, json=payload)
    response_data = response.json()
    return response_data.get("image_url")  # Извлеките URL изображения из ответа API

# Команда /generate для Telegram
async def handle_generate(update: Update, context):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Пожалуйста, укажите описание для генерации.")
        return

    await update.message.reply_text("Генерирую изображение, подождите...")
    image_url = generate_image(prompt)
    if image_url:
        await update.message.reply_photo(photo=image_url, caption="Вот ваше изображение!")
    else:
        await update.message.reply_text("Не удалось сгенерировать изображение.")

@app.route('/telegram/message', methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("generate", handle_generate))
    
    # Обработка входящего сообщения
    application.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

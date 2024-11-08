from telegram import Bot, Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler
import os
import requests
import asyncio
from flask import Flask, request

app = Flask(__name__)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

# Генерация изображения
def generate_image(prompt):
    api_url = "https://sd.klepinin.space/api/generate"  # Замените на актуальный эндпоинт из документации
    payload = {
        "prompt": prompt,
        "steps": 50,  # Задайте нужные параметры
        "width": 512,
        "height": 512,
    }
    response = requests.post(api_url, json=payload)
    response_data = response.json()
    return response_data.get("image_url")

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

# Асинхронная обработка вебхуков
@app.route('/telegram/message', methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    async def run_async_application():
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("generate", handle_generate))
        await application.process_update(update)

    asyncio.run(run_async_application())

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

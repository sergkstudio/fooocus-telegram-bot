from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from gradio_client import Client
import os

app = Flask(__name__)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

# Инициализация клиента Gradio
client = Client("https://sd.klepinin.space")

# Функция для генерации изображения
def generate_image(prompt):
    response = client.predict(prompt, fn_index=0)
    return response if isinstance(response, str) else None

def handle_generate(update, context):
    prompt = ' '.join(context.args)
    if not prompt:
        update.message.reply_text("Пожалуйста, укажите описание.")
        return

    update.message.reply_text("Генерирую изображение, подождите...")
    # Здесь должна быть функция для генерации изображения
    image_url = generate_image(prompt)
    update.message.reply_photo(photo=image_url, caption="Вот ваше изображение!")

@app.route('/telegram/message', methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot, None)
    dispatcher.add_handler(CommandHandler("generate", handle_generate))
    
    # Обработка входящего сообщения
    dispatcher.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

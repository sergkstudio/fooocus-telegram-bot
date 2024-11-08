from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import os

app = Flask(__name__)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

# Обработчик команды /generate
def handle_generate(update: Update, context):
    prompt = ' '.join(context.args)
    if not prompt:
        update.message.reply_text("Пожалуйста, укажите описание.")
        return

    update.message.reply_text("Генерирую изображение, подождите...")
    # Генерация изображения (замените на реальную логику)
    image_url = "https://example.com/generated_image.jpg"
    update.message.reply_photo(photo=image_url, caption="Вот ваше изображение!")

@app.route('/telegram/message', methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot, None)
    dispatcher.add_handler(CommandHandler("generate", handle_generate))
    
    # Обработка входящего обновления
    dispatcher.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

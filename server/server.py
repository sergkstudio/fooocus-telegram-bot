from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler
import os

app = Flask(__name__)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

def handle_generate(update: Update, context):
    prompt = ' '.join(context.args)
    if not prompt:
        update.message.reply_text("Пожалуйста, укажите описание.")
        return

    update.message.reply_text("Генерирую изображение, подождите...")
    # Здесь должна быть функция для генерации изображения
    image_url = "https://example.com/generated_image.jpg"  # Пример
    update.message.reply_photo(photo=image_url, caption="Вот ваше изображение!")

@app.route('/telegram/message', methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("generate", handle_generate))

    # Обработка обновления
    dispatcher.process_update(update)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

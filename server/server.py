from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
import os

app = Flask(__name__)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)  # Инициализация bot
    

# Обработчик команды /generate
async def handle_generate(update: Update, context):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Пожалуйста, укажите описание.")
        return

    await update.message.reply_text("Генерирую изображение, подождите...")
    # Генерация изображения (замените на реальную логику)
    image_url = "https://example.com/generated_image.jpg"
    await update.message.reply_photo(photo=image_url, caption="Вот ваше изображение!")

@app.route('/telegram/message', methods=['POST'])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("generate", handle_generate))
    
    # Обработка входящего обновления
    application.update_queue.put(update)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

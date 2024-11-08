from flask import Flask, request
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler

app = Flask(__name__)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Инициализация клиента Gradio
client = os.getenv("FOOCUS_URL")

# Функция для генерации изображения
def generate_image(prompt):
    response = client.predict(prompt, fn_index=0)
    return response if isinstance(response, str) else None

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
async def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("generate", handle_generate))
    
    # Обработка входящего сообщения
    await application.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)

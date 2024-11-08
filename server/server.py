from flask import Flask, request
import os
import asyncio
from telegram import Bot, Update
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
def telegram_webhook():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    data = request.get_json(force=True)
    bot = Bot(token=BOT_TOKEN)
    update = Update.de_json(data, bot)
    
    appl = Application.builder().token(BOT_TOKEN).build()
    appl.add_handler(CommandHandler("generate", handle_generate))
    loop.run_until_complete(appl.process_update(update))
        
    return 'OK', 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)

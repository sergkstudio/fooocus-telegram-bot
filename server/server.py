from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler
from gradio_client import Client
import asyncio
import os

app = Flask(__name__)
BOT_TOKEN = '8106530957:AAGTNBqOjVKXvma9EVl7efMR1Qcxow5BvkA'
bot = Bot(token=BOT_TOKEN)

# Инициализация клиента Gradio
client = Client("https://sd.klepinin.space")

# Функция для генерации изображения
def generate_image(prompt):
    response = client.predict(prompt, fn_index=0)
    return response if isinstance(response, str) else None

# Асинхронный обработчик команды /generate для Telegram
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
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Инициализация приложения Telegram с использованием initialize
    application = Application(BOT_TOKEN)
    application.add_handler(CommandHandler("generate", handle_generate))

    # Обработка обновлений
    loop.run_until_complete(application.process_update(update))
    
    return "OK", 200

if __name__ == "__main__":
    # Устанавливаем вебхук для бота
    asyncio.run(bot.set_webhook(url="https://sd.bot.klepinin.space/telegram/message"))
    app.run(host="0.0.0.0", port=5000)

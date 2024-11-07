from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from fooocus_client import generate_image_with_fooocus
import os

# Получаем токен бота из переменной окружения
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def handle_generate(update: Update, context: CallbackContext):
    prompt = ' '.join(context.args)
    if not prompt:
        update.message.reply_text("Пожалуйста, укажите описание.")
        return

    update.message.reply_text("Генерирую изображение, подождите...")
    image_url = generate_image_with_fooocus(prompt)

    if image_url:
        update.message.reply_photo(photo=image_url, caption="Вот ваше изображение!")
    else:
        update.message.reply_text("Ошибка при генерации изображения. Попробуйте позже.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("generate", handle_generate, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

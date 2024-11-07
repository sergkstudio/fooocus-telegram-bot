from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def handle_generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Пожалуйста, укажите описание.")
        return

    await update.message.reply_text("Генерирую изображение, подождите...")
    image_url = generate_image_with_fooocus(prompt)

    if image_url:
        await update.message.reply_photo(photo=image_url, caption="Вот ваше изображение!")
    else:
        await update.message.reply_text("Ошибка при генерации изображения. Попробуйте позже.")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("generate", handle_generate))

    application.run_polling()

if __name__ == "__main__":
    main()

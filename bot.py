import os
import logging
import base64
import tempfile
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gradio_client import Client
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FOOOCUS_API_URL = os.getenv('FOOOCUS_API_URL', 'http://localhost:7865')

client = Client(FOOOCUS_API_URL)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот для генерации изображений с помощью Fooocus. "
        "Просто отправь мне текстовое описание."
    )

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.strip()
    status_message = await update.message.reply_text('🔄 Генерация начата...')
    
    try:
        # Запуск генерации
        job = client.submit(
            prompt,
            "!",  # Negative prompt
            1,     # Number of images
            fn_index=83  # Индекс для запуска генерации
        )

        # Ожидаем завершения
        while not job.done():
            if job.status().code == "generating":
                await asyncio.sleep(2)
            else:
                break

        # Получаем результат
        result = client.predict(fn_index=86)  # Индекс для получения результатов
        logger.debug(f"Raw API response: {result}")

        # Извлекаем base64 из ответа
        if isinstance(result, list) and len(result) > 0:
            image_base64 = result[0]
            if isinstance(image_base64, str) and image_base64.startswith('data:image/png;base64,'):
                image_data = base64.b64decode(image_base64.split(",", 1)[1])
                
                # Отправляем изображение
                with BytesIO(image_data) as bio:
                    bio.seek(0)
                    await update.message.reply_photo(
                        photo=bio,
                        caption=f"Результат для: {prompt[:200]}"
                    )
                await status_message.delete()
                return

        raise ValueError("Не удалось получить изображение из ответа API")

    except Exception as e:
        logger.error(f'Ошибка генерации: {str(e)}', exc_info=True)
        await status_message.edit_text(f'❌ Ошибка: {str(e)}')

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    application.run_polling()

if __name__ == '__main__':
    main()
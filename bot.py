import os
import logging
import base64
import tempfile
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gradio_client import Client
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FOOOCUS_API_URL = os.getenv('FOOOCUS_API_URL', 'http://localhost:7865')

# Инициализация клиента Gradio
client = Client(FOOOCUS_API_URL)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        'Привет! Я бот для генерации изображений с помощью Fooocus. '
        'Просто отправь мне текстовое описание того, что ты хочешь увидеть.'
    )

async def handle_api_response(update: Update, result):
    """Обработка различных форматов ответов API"""
    try:
        # Вариант 1: Прямой base64 в ответе
        if isinstance(result, str) and result.startswith('data:image'):
            image_data = result.split(',', 1)[1]
            bio = BytesIO(base64.b64decode(image_data))
            await update.message.reply_photo(photo=bio)
            return True
        
        # Вариант 2: Словарь с данными изображения
        if isinstance(result, dict):
            if 'data' in result:
                bio = BytesIO(base64.b64decode(result['data']))
                await update.message.reply_photo(photo=bio)
                return True
            elif 'path' in result:
                with open(result['path'], 'rb') as f:
                    await update.message.reply_photo(photo=f)
                return True
        
        # Вариант 3: Вложенные структуры
        if isinstance(result, (list, tuple)):
            for item in result:
                if await handle_api_response(update, item):
                    return True
        
        # Логирование необработанных форматов
        logger.error(f"Неизвестный формат ответа: {type(result)} - {str(result)[:200]}")
        return False

    except Exception as e:
        logger.error(f"Ошибка обработки ответа: {str(e)}")
        return False

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Улучшенный обработчик генерации изображений"""
    prompt = update.message.text.strip()
    status_message = await update.message.reply_text('🔄 Генерирую изображение...')
    
    try:
        # Запуск генерации
        client.predict(
            # ... все параметры генерации ...
            fn_index=67
        )

        # Получение результатов
        result = client.predict(fn_index=68)
        logger.info(f"Raw API response: {result}")

        # Обработка результата
        if await handle_api_response(update, result):
            await status_message.delete()
        else:
            await status_message.edit_text('⚠️ Не удалось обработать результат генерации')

    except Exception as e:
        logger.error(f'Ошибка генерации: {str(e)}', exc_info=True)
        await status_message.edit_text(f'❌ Ошибка: {str(e)}')

def main():
    """Основная функция запуска бота"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
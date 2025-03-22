import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gradio_client import Client
from dotenv import load_dotenv
import tempfile

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

# Выводим список доступных эндпоинтов при запуске
logger.info("Доступные эндпоинты:")
try:
    # Получаем список всех доступных эндпоинтов
    endpoints = client.endpoints
    for endpoint_name in endpoints:
        logger.info(f"- {endpoint_name}")
except Exception as e:
    logger.error(f"Ошибка при получении списка эндпоинтов: {str(e)}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        'Привет! Я бот для генерации изображений с помощью Fooocus. '
        'Просто отправь мне текстовое описание того, что ты хочешь увидеть.'
    )

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений для генерации изображений"""
    prompt = update.message.text
    
    # Отправляем сообщение о начале генерации
    status_message = await update.message.reply_text('Генерирую изображение...')
    
    try:
        # Создаем временную директорию для сохранения изображения
        with tempfile.TemporaryDirectory() as temp_dir:
            # Создаем список аргументов для генерации изображения
            args = [prompt]  # начинаем с промпта
            args.extend([None] * 151)  # добавляем остальные аргументы как None
            
            # Запускаем генерацию изображения через Gradio API
            result = client.predict(*args, fn_index=67)
            
            if result and isinstance(result, str):
                # Отправляем изображение в чат
                await update.message.reply_photo(result)
                await status_message.delete()
            else:
                await status_message.edit_text('Ошибка: не удалось сгенерировать изображение')
                
    except Exception as e:
        logger.error(f'Ошибка при генерации изображения: {str(e)}')
        await status_message.edit_text('Произошла ошибка при генерации изображения')

def main():
    """Основная функция запуска бота"""
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 
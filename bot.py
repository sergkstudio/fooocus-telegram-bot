import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
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
FOOOCUS_API_URL = os.getenv('FOOOCUS_API_URL', 'http://localhost:8188')

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
        # Отправляем запрос к Fooocus API
        response = requests.post(
            f'{FOOOCUS_API_URL}/generate',
            json={'prompt': prompt}
        )
        
        if response.status_code == 200:
            # Получаем URL сгенерированного изображения
            image_url = response.json().get('image_url')
            
            if image_url:
                # Отправляем изображение в чат
                await update.message.reply_photo(image_url)
                await status_message.delete()
            else:
                await status_message.edit_text('Ошибка: не удалось получить URL изображения')
        else:
            await status_message.edit_text(f'Ошибка при генерации изображения: {response.status_code}')
            
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
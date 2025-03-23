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
            False,  # Generate Image Grid for Each Batch
            prompt,
            "!",  # Negative Prompt
            ["Fooocus V2"],  # Selected Styles
            "Quality",  # Performance
            "1280×768",  # Aspect Ratios
            1,  # Image Number
            "png",  # Output Format
            "0",  # Seed
            False,  # Read wildcards in order
            2,  # Image Sharpness
            7,  # Guidance Scale
            "juggernautXL_v8Rundiffusion.safetensors",  # Base Model
            "None",  # Refiner
            0.5,  # Refiner Switch At
            True, "None", -2,  # LoRA 1
            True, "None", -2,  # LoRA 2
            True, "None", -2,  # LoRA 3
            True, "None", -2,  # LoRA 4
            True, "None", -2,  # LoRA 5
            False, "", "Disabled", "", ["Left"], "", "", "",
            True, True, True, False, 1.5, 0.8, 0.3, 7, 2,
            "dpmpp_2m_sde_gpu", "karras", "Default (model)",
            -1, -1, -1, -1, -1, -1, False, False, False, False,
            64, 128, "joint", 0.25, False, 1.01, 1.02, 0.99, 0.95,
            False, False, "v2.6", 1, 0.618,
            False, False, 0, False, False, "fooocus",
            "", 0, 0, "ImagePrompt",
            "", 0, 0, "ImagePrompt",
            "", 0, 0, "ImagePrompt",
            "", 0, 0, "ImagePrompt",
            False, 0, False, "",
            False, "Disabled", "Before First Enhancement", "Original Prompts",
            False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True,
            "v2.6", 1, 0.618, 0, False,
            False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True,
            "v2.6", 1, 0.618, 0, False,
            False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True,
            "v2.6", 1, 0.618, 0, False,
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
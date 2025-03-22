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
            # Первый вызов API для генерации изображения
            result = client.predict(
                False,  # Generate Image Grid for Each Batch
                prompt,  # Prompt
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
                "animaPencilXL_v500.safetensors",  # Base Model
                "None",  # Refiner
                0.5,  # Refiner Switch At
                # LoRA settings
                True, "None", -2,  # LoRA 1
                True, "None", -2,  # LoRA 2
                True, "None", -2,  # LoRA 3
                True, "None", -2,  # LoRA 4
                True, "None", -2,  # LoRA 5
                # Input Image settings
                False, "", "Disabled", "", ["Left"], "", "", "",
                # Developer Debug Mode
                True, True, True, False, 1.5, 0.8, 0.3, 7, 2,
                "dpmpp_2m_sde_gpu", "karras", "Default (model)",
                -1, -1, -1, -1, -1, -1, False, False, False, False,
                64, 128, "joint", 0.25, False, 1.01, 1.02, 0.99, 0.95,
                False, False, "v2.6", 1, 0.618,
                # MISC
                False, False, 0, False, False, "fooocus",
                # Image Prompt settings
                "", 0, 0, "ImagePrompt",  # Image 1
                "", 0, 0, "ImagePrompt",  # Image 2
                "", 0, 0, "ImagePrompt",  # Image 3
                "", 0, 0, "ImagePrompt",  # Image 4
                False, 0, False, "",
                # Enhance settings
                False, "Disabled", "Before First Enhancement", "Original Prompts",
                # Enhance #1
                False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True,
                "v2.6", 1, 0.618, 0, False,
                # Enhance #2
                False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True,
                "v2.6", 1, 0.618, 0, False,
                # Enhance #3
                False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True,
                "v2.6", 1, 0.618, 0, False,
                fn_index=67
            )
            
            logger.info(f"Результат первого вызова API: {result}")
            
            # Второй вызов API
            result = client.predict(fn_index=68)
            logger.info(f"Результат второго вызова API: {result}")
            
            # Проверяем тип результата и его содержимое
            if isinstance(result, dict):
                logger.info(f"Ключи в результате: {result.keys()}")
                if 'image' in result:
                    image_path = result['image']
                    logger.info(f"Путь к изображению: {image_path}")
                    # Отправляем изображение в чат
                    await update.message.reply_photo(image_path)
                    await status_message.delete()
                else:
                    logger.error(f"В результате нет ключа 'image'. Содержимое: {result}")
                    await status_message.edit_text('Ошибка: не удалось сгенерировать изображение')
            else:
                logger.error(f"Неверный тип результата: {type(result)}. Значение: {result}")
                await status_message.edit_text('Ошибка: не удалось сгенерировать изображение')
                
    except Exception as e:
        logger.error(f'Ошибка при генерации изображения: {str(e)}', exc_info=True)
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
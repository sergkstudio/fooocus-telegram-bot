import os
import logging
import asyncio  # Добавлен недостающий импорт
import base64
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

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FOOOCUS_API_URL = os.getenv('FOOOCUS_API_URL', 'http://localhost:7865')

client = Client(FOOOCUS_API_URL)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Привет! Отправь мне текстовое описание для генерации изображения.'
    )

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.strip()
    status_message = await update.message.reply_text('🔄 Генерация начата...')
    
    try:
        # Создаем job для асинхронной обработки
        job = client.submit(
            False,  # Generate Image Grid
            prompt,
            "!",  # Negative Prompt
            ["Fooocus V2"],  # Styles
            "Quality",  # Performance
            "1280×768",  # Aspect Ratio
            1,  # Image Number
            "png",  # Output Format
            "0",  # Seed
            False,  # Read Wildcards Order
            2,  # Sharpness
            7,  # Guidance Scale
            "juggernautXL_v8Rundiffusion.safetensors",  # Base Model
            "None",  # Refiner
            0.5,  # Refiner Switch
            True, "None", -2,  # LoRA 1
            True, "None", -2,  # LoRA 2
            True, "None", -2,  # LoRA 3
            True, "None", -2,  # LoRA 4
            True, "None", -2,  # LoRA 5
            False, "", "Disabled", "", ["Left"], "", "", "",  # Image Inputs
            True, True, True, False, 1.5, 0.8, 0.3, 7, 2,  # Debug Settings
            "dpmpp_2m_sde_gpu", "karras", "Default (model)",  # Sampler
            -1, -1, -1, -1, -1, -1, False, False, False, False,  # Overrides
            64, 128, "joint", 0.25, False, 1.01, 1.02, 0.99, 0.95,  # Advanced
            False, False, "v2.6", 1, 0.618,  # Misc
            False, False, 0, False, False, "fooocus",  # Metadata
            "", 0, 0, "ImagePrompt",  # Image Prompts
            "", 0, 0, "ImagePrompt",
            "", 0, 0, "ImagePrompt",
            "", 0, 0, "ImagePrompt",
            False, 0, False, "",  # Enhance
            False, "Disabled", "Before First Enhancement", "Original Prompts",  # Enhance
            False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True,  # Enhance
            "v2.6", 1, 0.618, 0, False,
            False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True,
            "v2.6", 1, 0.618, 0, False,
            False, "", "", "", "sam", "full", "vit_b", 0.25, 0.3, 0, True,
            "v2.6", 1, 0.618, 0, False,
            fn_index=67
        )

        # Обработка событий
        final_result = None
        while not job.done():
            await asyncio.sleep(0.1)
            for event in job.communicator.events:
                if event.event == "process_completed":
                    final_result = job.outputs()

        # Обработка результата
        if final_result:
            images = final_result[2]  # Finished Images Gallery
            if images and len(images) > 0:
                first_image = images[0]
                
                # Получаем base64 из данных изображения
                if isinstance(first_image, dict) and 'data' in first_image:
                    image_bytes = base64.b64decode(first_image['data'])
                    bio = BytesIO(image_bytes)
                    bio.seek(0)
                    
                    await update.message.reply_photo(
                        photo=bio,
                        caption=f"Результат: {prompt[:200]}"
                    )
                    await status_message.delete()
                    return

        await status_message.edit_text('⚠️ Не удалось сгенерировать изображение')

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
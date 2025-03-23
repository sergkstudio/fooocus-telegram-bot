import os
import logging
import asyncio
import base64
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
        'Привет! Отправь мне текстовое описание для генерации изображения.'
    )

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.strip()
    status_message = await update.message.reply_text('🔄 Генерация начата...')
    
    try:
        # Первый вызов - запуск генерации
        client.predict(
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

        # Второй вызов - получение результатов
        result = client.predict(fn_index=68)
        logger.info(f"API Response Structure: {type(result)} - {str(result)[:500]}")

        # Обработка структуры ответа
        if isinstance(result, tuple) and len(result) >= 3:
            gallery = result[2]  # Индекс 2 соответствует Finished Images Gallery
            if isinstance(gallery, list) and len(gallery) > 0:
                first_image = gallery[0]
                if isinstance(first_image, dict):
                    if 'data' in first_image:
                        # Декодирование base64
                        image_data = first_image['data'].split(",", 1)[1]
                        image_bytes = base64.b64decode(image_data)
                    elif 'name' in first_image:
                        # Чтение из файла
                        with open(first_image['name'], "rb") as f:
                            image_bytes = f.read()
                    else:
                        raise ValueError("Неизвестный формат изображения")
                    
                    # Отправка изображения
                    await update.message.reply_photo(
                        photo=BytesIO(image_bytes),
                        caption=f"Результат: {prompt[:200]}"
                    )
                    await status_message.delete()
                    return

        raise ValueError("Изображение не найдено в ответе API")

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
import os
import logging
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

# Инициализация клиента Gradio
GRADIO_URL = os.getenv('GRADIO_URL', 'http://localhost:7865/')
client = Client(GRADIO_URL)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        'Привет! Я бот для генерации изображений через Fooocus. '
        'Отправь мне промпт, и я сгенерирую изображение.'
    )

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений для генерации изображений"""
    prompt = update.message.text
    
    # Отправляем сообщение о начале генерации
    status_message = await update.message.reply_text('Начинаю генерацию изображения...')
    
    try:
        # Запускаем генерацию (fn_index=67)
        job = client.predict(
            True,  # Generate Image Grid
            prompt,  # Positive prompt
            "",  # Negative prompt
            ["Fooocus V2"],  # Style
            "Quality",  # Performance
            "704×1408",  # Aspect ratio
            1,  # Number of images
            "png",  # Output format
            "",  # Seed
            True,  # Read wildcards
            0,  # Sharpness
            1,  # Guidance scale
            "juggernautXL_v8Rundiffusion.safetensors",  # Base model
            "None",  # Refiner
            0.1,  # Refiner switch at
            True,  # Enable refiner
            "None",  # LoRA 1
            -2,  # LoRA 1 weight
            True,  # Enable LoRA 2
            "None",  # LoRA 2
            -2,  # LoRA 2 weight
            True,  # Enable LoRA 3
            "None",  # LoRA 3
            -2,  # LoRA 3 weight
            True,  # Enable LoRA 4
            "None",  # LoRA 4
            -2,  # LoRA 4 weight
            True,  # Enable LoRA 5
            "None",  # LoRA 5
            -2,  # LoRA 5 weight
            False,  # Input image
            "",  # Input image prompt
            "Disabled",  # Upscale or variation
            None,  # Image
            ["Left"],  # Outpaint direction
            None,  # Image
            "",  # Inpaint additional prompt
            None,  # Mask
            True,  # Disable preview
            True,  # Disable intermediate results
            True,  # Disable seed increment
            True,  # Black out NSFW
            0.1,  # Positive ADM guidance
            0.1,  # Negative ADM guidance
            0,  # ADM guidance end at step
            1,  # CFG mimicking
            1,  # CLIP skip
            "euler",  # Sampler
            "normal",  # Scheduler
            "Default (model)",  # VAE
            -1,  # Forced sampling steps
            -1,  # Forced refiner switch step
            -1,  # Forced width
            -1,  # Forced height
            -1,  # Forced vary strength
            -1,  # Forced upscale strength
            True,  # Mixing image prompt and vary/upscale
            True,  # Mixing image prompt and inpaint
            True,  # Debug preprocessors
            True,  # Skip preprocessors
            1,  # Canny low threshold
            1,  # Canny high threshold
            "joint",  # Refiner swap method
            0,  # ControlNet softness
            True,  # Enable advanced features
            0,  # B1
            0,  # B2
            0,  # S1
            0,  # S2
            True,  # Debug inpaint preprocessing
            True,  # Disable initial latent
            "None",  # Inpaint engine
            0,  # Inpaint denoising strength
            0,  # Inpaint respective field
            True,  # Enable advanced masking
            True,  # Invert mask
            -64,  # Mask erode/dilate
            True,  # Save only final
            True,  # Save metadata
            "fooocus",  # Metadata scheme
            None,  # Image
            0,  # Stop at
            0,  # Weight
            "ImagePrompt",  # Type
            None,  # Image
            0,  # Stop at
            0,  # Weight
            "ImagePrompt",  # Type
            None,  # Image
            0,  # Stop at
            0,  # Weight
            "ImagePrompt",  # Type
            None,  # Image
            0,  # Stop at
            0,  # Weight
            "ImagePrompt",  # Type
            True,  # Debug GroundingDINO
            -64,  # GroundingDINO box erode/dilate
            True,  # Debug enhance masks
            None,  # Use with enhance
            True,  # Enhance
            "Disabled",  # Upscale or variation
            "Before First Enhancement",  # Order of processing
            "Original Prompts",  # Prompt
            True,  # Enable
            "",  # Detection prompt
            "",  # Enhancement positive prompt
            "",  # Enhancement negative prompt
            "u2net",  # Mask generation model
            "full",  # Cloth category
            "vit_b",  # SAM model
            0,  # Text threshold
            0,  # Box threshold
            0,  # Max detections
            True,  # Disable initial latent
            "None",  # Inpaint engine
            0,  # Inpaint denoising strength
            0,  # Inpaint respective field
            -64,  # Mask erode/dilate
            True,  # Invert mask
            True,  # Enable
            "",  # Detection prompt
            "",  # Enhancement positive prompt
            "",  # Enhancement negative prompt
            "u2net",  # Mask generation model
            "full",  # Cloth category
            "vit_b",  # SAM model
            0,  # Text threshold
            0,  # Box threshold
            0,  # Max detections
            True,  # Disable initial latent
            "None",  # Inpaint engine
            0,  # Inpaint denoising strength
            0,  # Inpaint respective field
            -64,  # Mask erode/dilate
            True,  # Invert mask
            True,  # Enable
            "",  # Detection prompt
            "",  # Enhancement positive prompt
            "",  # Enhancement negative prompt
            "u2net",  # Mask generation model
            "full",  # Cloth category
            "vit_b",  # SAM model
            0,  # Text threshold
            0,  # Box threshold
            0,  # Max detections
            True,  # Disable initial latent
            "None",  # Inpaint engine
            0,  # Inpaint denoising strength
            0,  # Inpaint respective field
            -64,  # Mask erode/dilate
            True,  # Invert mask
            fn_index=67
        )

        # Получаем результат (fn_index=68)
        result = client.predict(fn_index=68)
        
        # Отправляем сгенерированное изображение
        if result and len(result) > 2:
            image_path = result[2]  # Путь к сгенерированному изображению
            await update.message.reply_photo(photo=open(image_path, 'rb'))
        else:
            await update.message.reply_text('Не удалось сгенерировать изображение.')
            
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        await update.message.reply_text('Произошла ошибка при генерации изображения.')
    finally:
        await status_message.delete()

def main():
    """Запуск бота"""
    # Получаем токен из переменных окружения
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_TOKEN не установлен в переменных окружения")

    # Создаем приложение
    application = Application.builder().token(token).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 
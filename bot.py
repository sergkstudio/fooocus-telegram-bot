import os
import logging
import random
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
        # Генерируем случайное значение для seed
        seed = str(random.randint(1, 1000000))
        
        # Запускаем генерацию (fn_index=67)
        job = client.predict(
            False,  # Generate Image Grid
            prompt,  # Positive prompt
            "!",  # Negative prompt
            ["Fooocus V2"],  # Style
            "Speed",  # Performance
            "1280×768",  # Aspect ratio
            1,  # Number of images
            "png",  # Output format
            seed,  # Seed
            False,  # Read wildcards
            2,  # Sharpness
            7,  # Guidance scale
            "juggernautXL_v8Rundiffusion.safetensors",  # Base model
            "None",  # Refiner
            0.5,  # Refiner switch at
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
            "",  # Image
            ["Left"],  # Outpaint direction
            "",  # Image
            "",  # Inpaint additional prompt
            "",  # Mask
            True,  # Disable preview
            True,  # Disable intermediate results
            True,  # Disable seed increment
            False,  # Black out NSFW
            1.5,  # Positive ADM guidance
            0.8,  # Negative ADM guidance
            0.3,  # ADM guidance end at step
            7,  # CFG mimicking
            2,  # CLIP skip
            "dpmpp_2m_sde_gpu",  # Sampler
            "karras",  # Scheduler
            "Default (model)",  # VAE
            -1,  # Forced sampling steps
            -1,  # Forced refiner switch step
            -1,  # Forced width
            -1,  # Forced height
            -1,  # Forced vary strength
            -1,  # Forced upscale strength
            False,  # Mixing image prompt and vary/upscale
            False,  # Mixing image prompt and inpaint
            False,  # Debug preprocessors
            False,  # Skip preprocessors
            64,  # Canny low threshold
            128,  # Canny high threshold
            "joint",  # Refiner swap method
            0.25,  # ControlNet softness
            False,  # Enable advanced features
            1.01,  # B1
            1.02,  # B2
            0.99,  # S1
            0.95,  # S2
            False,  # Debug inpaint preprocessing
            False,  # Disable initial latent
            "v2.6",  # Inpaint engine
            1,  # Inpaint denoising strength
            0.618,  # Inpaint respective field
            False,  # Enable advanced masking
            False,  # Invert mask
            0,  # Mask erode/dilate
            False,  # Save only final
            False,  # Save metadata
            "fooocus",  # Metadata scheme
            "",  # Image
            0,  # Stop at
            0,  # Weight
            "ImagePrompt",  # Type
            "",  # Image
            0,  # Stop at
            0,  # Weight
            "ImagePrompt",  # Type
            "",  # Image
            0,  # Stop at
            0,  # Weight
            "ImagePrompt",  # Type
            "",  # Image
            0,  # Stop at
            0,  # Weight
            "ImagePrompt",  # Type
            False,  # Debug GroundingDINO
            0,  # GroundingDINO box erode/dilate
            False,  # Debug enhance masks
            "",  # Use with enhance
            False,  # Enhance
            "Disabled",  # Upscale or variation
            "Before First Enhancement",  # Order of processing
            "Original Prompts",  # Prompt
            False,  # Enable
            "",  # Detection prompt
            "",  # Enhancement positive prompt
            "",  # Enhancement negative prompt
            "sam",  # Mask generation model
            "full",  # Cloth category
            "vit_b",  # SAM model
            0.25,  # Text threshold
            0.3,  # Box threshold
            0,  # Max detections
            True,  # Disable initial latent
            "v2.6",  # Inpaint engine
            1,  # Inpaint denoising strength
            0.618,  # Inpaint respective field
            0,  # Mask erode/dilate
            False,  # Invert mask
            False,  # Enable
            "",  # Detection prompt
            "",  # Enhancement positive prompt
            "",  # Enhancement negative prompt
            "sam",  # Mask generation model
            "full",  # Cloth category
            "vit_b",  # SAM model
            0.25,  # Text threshold
            0.3,  # Box threshold
            0,  # Max detections
            True,  # Disable initial latent
            "v2.6",  # Inpaint engine
            1,  # Inpaint denoising strength
            0.618,  # Inpaint respective field
            0,  # Mask erode/dilate
            False,  # Invert mask
            False,  # Enable
            "",  # Detection prompt
            "",  # Enhancement positive prompt
            "",  # Enhancement negative prompt
            "sam",  # Mask generation model
            "full",  # Cloth category
            "vit_b",  # SAM model
            0.25,  # Text threshold
            0.3,  # Box threshold
            0,  # Max detections
            True,  # Disable initial latent
            "v2.6",  # Inpaint engine
            1,  # Inpaint denoising strength
            0.618,  # Inpaint respective field
            0,  # Mask erode/dilate
            False,  # Invert mask
            fn_index=67
        )

        # Получаем результат (fn_index=68)
        result = client.predict(fn_index=68)
        logger.info(f"Fooocus API result: {result}")
        
        # Очищаем кэш (fn_index=69-72)
        for i in range(69, 73):
            client.predict(fn_index=i)
        
        # Получаем путь к изображению из результата
        if result and isinstance(result, (list, tuple)) and len(result) >= 4:
            gallery_result = result[3]  # Gallery component
            if isinstance(gallery_result, dict) and "value" in gallery_result and len(gallery_result["value"]) > 0:
                image_info = gallery_result["value"][0]
                if isinstance(image_info, dict) and "name" in image_info:
                    image_path = image_info["name"]
                    try:
                        with open(image_path, 'rb') as photo:
                            await update.message.reply_photo(photo=photo)
                    except Exception as e:
                        logger.error(f"Error sending photo: {e}")
                        await update.message.reply_text('Не удалось отправить сгенерированное изображение.')
                else:
                    logger.error(f"Invalid image info format: {image_info}")
                    await update.message.reply_text('Не удалось сгенерировать изображение: неверный формат информации об изображении.')
            else:
                logger.error(f"Invalid gallery result format: {gallery_result}")
                await update.message.reply_text('Не удалось сгенерировать изображение: неверный формат результата галереи.')
        else:
            logger.error(f"Invalid result format: {result}")
            await update.message.reply_text('Не удалось сгенерировать изображение: неверный формат результата.')
            
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
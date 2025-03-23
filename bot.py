import os
import logging
import random
import requests
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
logger.info(f"Initializing Gradio client with URL: {GRADIO_URL}")

# Проверяем доступность сервера
try:
    response = requests.get(GRADIO_URL)
    if response.status_code == 200:
        logger.info("Fooocus server is available")
    else:
        logger.error(f"Fooocus server returned status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    logger.error(f"Failed to connect to Fooocus server: {e}")
    raise

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
    logger.info(f"Received prompt: {prompt}")
    
    # Отправляем сообщение о начале генерации
    status_message = await update.message.reply_text('Начинаю генерацию изображения...')
    
    try:
        # Генерируем случайное значение для seed
        seed = str(random.randint(1, 1000000))
        logger.info(f"Generated seed: {seed}")
        
        logger.info("Starting image generation with parameters:")
        logger.info(f"Prompt: {prompt}")
        logger.info(f"Seed: {seed}")
        logger.info(f"GRADIO_URL: {GRADIO_URL}")
        
        # Запускаем генерацию (fn_index=67)
        logger.info("Calling client.predict with fn_index=67")
        result = client.predict(
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
            False,  # Disable initial latent
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
            False,  # Disable initial latent
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
            False,  # Disable initial latent
            "v2.6",  # Inpaint engine
            1,  # Inpaint denoising strength
            0.618,  # Inpaint respective field
            0,  # Mask erode/dilate
            False,  # Invert mask
            fn_index=67
        )
        
        logger.info("Received result from client.predict")
        logger.info(f"Result type: {type(result)}")
        logger.info(f"Result: {result}")
        
        # Проверяем, что результат не None
        if result is None:
            logger.error("Received None result from client.predict")
            await update.message.reply_text('Ошибка: не получен результат от API.')
            return
            
        # Проверяем, что результат содержит путь к изображению
        if isinstance(result, (list, tuple)) and len(result) >= 3:
            image_path = result[2]
            logger.info(f"Found image path: {image_path}")
            
            # Формируем URL для скачивания изображения
            image_url = f"{GRADIO_URL}file={image_path}"
            logger.info(f"Image URL: {image_url}")
            
            # Скачиваем изображение
            response = requests.get(image_url)
            if response.status_code == 200:
                # Сохраняем изображение во временный файл
                with open('temp_image.png', 'wb') as f:
                    f.write(response.content)
                logger.info("Image downloaded successfully")
                
                # Отправляем изображение пользователю
                with open('temp_image.png', 'rb') as photo:
                    await update.message.reply_photo(photo=photo)
                logger.info("Image sent to user")
                
                # Удаляем временный файл
                if os.path.exists('temp_image.png'):
                    os.remove('temp_image.png')
                    logger.info("Temporary file deleted")
            else:
                logger.error(f"Failed to download image. Status code: {response.status_code}")
                await update.message.reply_text('Ошибка при скачивании изображения.')
        else:
            logger.error(f"Unexpected result format: {result}")
            await update.message.reply_text('Ошибка: неверный формат результата от API.')
            
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Error args: {e.args}")
        await update.message.reply_text('Произошла ошибка при генерации изображения.')
    finally:
        await status_message.delete()

def main():
    """Основная функция запуска бота"""
    # Получаем токен бота из переменных окружения
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    
    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 
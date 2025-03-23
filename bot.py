import os
import logging
import random
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gradio_client import Client
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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
client = Client(GRADIO_URL, serialize=False)

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
            True,  # Generate Image Grid for Each Batch
            prompt,  # Positive prompt
            "",  # Negative prompt
            ["Fooocus V2"],  # Selected Styles
            "Hyper-SD",  # Performance
            "1152×896 ∣ 9:7",  # Aspect Ratios
            1,  # Image Number
            "png",  # Output Format
            "",  # Seed
            True,  # Read wildcards in order
            2,  # Image Sharpness
            4,  # Guidance Scale
            "juggernautXL_v8Rundiffusion.safetensors",  # Base Model
            "None",  # Refiner
            0.1,  # Refiner Switch At
            True,  # Enable LoRA 1
            "sd_xl_offset_example-lora_1.0.safetensors",  # LoRA 1
            0.1,  # LoRA 1 Weight
            True,  # Enable LoRA 2
            "None",  # LoRA 2
            1,  # LoRA 2 Weight
            True,  # Enable LoRA 3
            "None",  # LoRA 3
            1,  # LoRA 3 Weight
            True,  # Enable LoRA 4
            "None",  # LoRA 4
            1,  # LoRA 4 Weight
            True,  # Enable LoRA 5
            "None",  # LoRA 5
            1,  # LoRA 5 Weight
            True,  # Input Image
            "",  # Input Image Prompt
            "Disabled",  # Upscale or Variation
            "",  # Image
            ["Left"],  # Outpaint Direction
            "",  # Image
            "",  # Inpaint Additional Prompt
            "",  # Mask
            True,  # Disable Preview
            True,  # Disable Intermediate Results
            False,  # Disable seed increment
            False,  # Black Out NSFW
            1.5,  # Positive ADM Guidance Scaler
            0.8,  # Negative ADM Guidance Scaler
            0.3,  # ADM Guidance End At Step
            7,  # CFG Mimicking from TSNR
            2,  # CLIP Skip
            "dpmpp_2m_sde_gpu",  # Sampler
            "karras",  # Scheduler
            "Default (model)",  # VAE
            -1,  # Forced Overwrite of Sampling Step
            -1,  # Forced Overwrite of Refiner Switch Step
            -1,  # Forced Overwrite of Generating Width
            -1,  # Forced Overwrite of Generating Height
            -1,  # Forced Overwrite of Denoising Strength of "Vary"
            -1,  # Forced Overwrite of Denoising Strength of "Upscale"
            False,  # Mixing Image Prompt and Vary/Upscale
            True,  # Mixing Image Prompt and Inpaint
            False,  # Debug Preprocessors
            False,  # Skip Preprocessors
            64,  # Canny Low Threshold
            128,  # Canny High Threshold
            "joint",  # Refiner swap method
            0.25,  # Softness of ControlNet
            False,  # FreeU Enabled
            0,  # FreeU B1
            0,  # FreeU B2
            0,  # FreeU S1
            0,  # FreeU S2
            False,  # Debug Inpaint Preprocessing
            False,  # Disable initial latent in inpaint
            "v2.6",  # Inpaint Engine
            1,  # Inpaint Denoising Strength
            0.618,  # Inpaint Respective Field
            False,  # Enable Mask Upload
            False,  # Invert Mask
            6,  # Mask Erode or Dilate
            False,  # Save Metadata to Images
            "fooocus",  # Metadata Scheme
            "",  # Image Prompt 1 Image
            0.9,  # Image Prompt 1 Stop At
            0.75,  # Image Prompt 1 Weight
            "FaceSwap",  # Image Prompt 1 Type
            "",  # Image Prompt 2 Image
            0,  # Image Prompt 2 Stop At
            0,  # Image Prompt 2 Weight
            "ImagePrompt",  # Image Prompt 2 Type
            "",  # Image Prompt 3 Image
            0,  # Image Prompt 3 Stop At
            0,  # Image Prompt 3 Weight
            "ImagePrompt",  # Image Prompt 3 Type
            "",  # Image Prompt 4 Image
            0,  # Image Prompt 4 Stop At
            0,  # Image Prompt 4 Weight
            "ImagePrompt",  # Image Prompt 4 Type
            fn_index=67
        )

        # Получаем результат
        result = client.predict(fn_index=68)
        logger.info(f"API result: {result}")
        
        # Получаем изображение из результата
        img = mpimg.imread(result[2])
        
        # Сохраняем изображение во временный файл
        plt.imsave('temp_image.png', img)
        
        # Отправляем изображение в Telegram
        with open('temp_image.png', 'rb') as photo:
            await update.message.reply_photo(photo=photo)
            
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        await update.message.reply_text('Произошла ошибка при генерации изображения.')
    finally:
        await status_message.delete()
        # Удаляем временный файл
        if os.path.exists('temp_image.png'):
            os.remove('temp_image.png')

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
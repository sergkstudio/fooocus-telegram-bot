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
				False,			# 'Generate Image Grid for Each Batch'
				prompt,	# str in 'Prompt' Textbox
				"!",			# 'Negative Prompt' Textbox 
				["Fooocus V2"],	# List[str] in 'Selected Styles' Checkboxgroup
				"Quality",		# str in 'Performance' Radio
				"1280×768",	   # str in 'Aspect Ratios' Radio
				1,				# [1, 32] in 'Image Number' Slider
				"png",			# 'Output Format' Radio
				"0",			# 'Seed' Textbox
				False,			# 'Read wildcards in order' Checkbox
				2,				# [0.0, 30.0] in 'Image Sharpness' Slider
				7,				# [1.0, 30.0] in 'Guidance Scale' Slider
				"animaPencilXL_v500.safetensors",	# 'Base Model (SDXL only)' Dropdown
				"None",			# 'Refiner (SDXL or SD 1.5)' Dropdown
				0.5,			# [0.1, 1.0] in 'Refiner Switch At' Slider
                ################################################################
                # LoRA
				True,	# 'LoRA 1 Enable'
				"None",	# 'LoRA 1' Dropdown
				-2,		# [-2, 2] in 'LoRA 1 Weight'
				True,	# 'LoRA 2 Enable'
				"None",	# 'LoRA 2' Dropdown
				-2,		# [-2, 2] in 'LoRA 2 Weight'
				True,	# 'LoRA 3 Enable'
				"None",	# 'LoRA 3' Dropdown 
				-2,		# [-2, 2] in 'LoRA 3 Weight'
				True,	# 'LoRA 4 Enable'
				"None",	# 'LoRA 4' Dropdown
				-2,		# [-2, 2] in 'LoRA 4 Weight'
				True,	# 'LoRA 5 Enable'
				"None",	# 'LoRA 5' Dropdown component
				-2,		# [-2, 2] in 'LoRA 5 Weight'
                ################################################################
                # Input Image
				False,		# bool in 'Input Image' Checkbox
				"",			# str in 'parameter_212' Textbox
				"Disabled",	# 'Upscale or Variation:'
				"", 		# 'Upscale or Variation' Image
				["Left"],	# 'Outpaint Direction'
				"",			# Inpaint or Outpaint 'Image'
				"",			# 'Inpaint Additional Prompt'
				"",			# Inpaint or Outpaint 'Mask Upload' Image
                ################################################################
                # Developer Debug Mode
				True,	# 'Disable Preview'
				True,	# 'Disable Intermediate Results'
				True,	# 'Disable seed increment'
				False,	# 'Black Out NSFW'
				1.5,	# [0.1, 3.0] in 'Positive ADM Guidance Scaler'
				0.8,	# [0.1, 3.0] in 'Negative ADM Guidance Scaler'
				0.3,	# [0.0, 1.0] in 'ADM Guidance End At Step'
				7,		# [1.0, 30.0] in 'CFG Mimicking from TSNR'
				2,		# [1, 12] in 'CLIP Skip'
				"dpmpp_2m_sde_gpu",	# 'Sampler'
				"karras",	# 'Scheduler'
				"Default (model)",	# 'VAE'
				-1,		# [-1, 200] in 'Forced Overwrite of Sampling Step'
				-1,		# [-1, 200] in 'Forced Overwrite of Refiner Switch Step'
				-1,		# [-1, 2048] in 'Forced Overwrite of Generating Width'
				-1,		# [-1, 2048] in 'Forced Overwrite of Generating Height'
				-1,		# [-1, 1.0] in 'Forced Overwrite of Denoising Strength of "Vary"'
				-1,		# [-1, 1.0] in 'Forced Overwrite of Denoising Strength of "Upscale"'
				False,	# 'Mixing Image Prompt and Vary/Upscale'
				False,	# 'Mixing Image Prompt and Inpaint'
				False,	# 'Debug Preprocessors'
				False,	# 'Skip Preprocessors'
				64,		# [1, 255] in 'Canny Low Threshold'
				128,	# [1, 255] in 'Canny High Threshold'
				"joint",# 'Refiner swap method'
				0.25,	# [0.0, 1.0] in 'Softness of ControlNet'
				False,	# 'FreeU Enabled'
				1.01,	# [0, 2] in 'FreeU B1'
				1.02,	# [0, 2] in 'FreeU B2'
				0.99,	# [0, 4] in 'FreeU S1'
				0.95,	# [0, 4] in 'FreeU S2'
				False,	# 'Debug Inpaint Preprocessing'
				False,	# 'Disable initial latent in inpaint'
				"v2.6",	# 'Inpaint Engine'
				1,		# [0.0, 1.0] in 'Inpaint Denoising Strength'
				0.618,	# [0.0, 1.0] in 'Inpaint Respective Field'
                ################################################################
                # MISC
				False,	# 'Input Image: Inpaint or Outpaint: Enable Advanced Masking Features'
				False,	# 'Input Image: Inpaint or Outpaint: Invert Mask When Generating'
				0,		# [-64, 64] in 'Mask Erode or Dilate'
				False,	# 'Developer Debug Mode: Save only final enhanced image'
				False,	# 'Developer Debug Mode: Save Metadata to Images'
				"fooocus",	# str in 'Metadata Scheme' Radio
                ################################################################
                # Image
                # Image Prompt Image 1
				"",	# Image
				0,	# [0, 1.0] in 'Stop At'
				0,	# [0, 2.0] in 'Weight'
				"ImagePrompt",	# 'Type' Radio
                # Image Prompt Image 2
				"",	# 'Image 2' Image
				0,	# [0, 1.0] in 'Stop At'
				0,	# [0, 2.0] in 'Weight'
				"ImagePrompt",	# 'Type' Radio
                # Image Prompt Image 3
				"",	# 'Image 3' Image
				0,	# [0, 1.0] in 'Stop At'
				0,	# [0, 2.0] in 'Weight'
				"ImagePrompt",	# 'Type' Radio
                # Image Prompt Image 4
				"",	# 'Image 4' Image
				0,	# [0, 1.0] in 'Stop At'
				0,	# [0, 2.0] in 'Weight'
				"ImagePrompt",	# 'Type' Radio
				False,	# 'Developer Debug Mode: Debug GroundingDINO'
				0,		# [-64, 64] in 'Developer Debug Mode: GroundingDINO Box Erode or Dilate'
				False,	# 'Developer Debug Mode: Debug Enhance Masks'
				"",		# 'Input Image/Enhance: Use with Enhance, skips image generation' Image
                ################################################################
                # Enhance
				False,	# 'Enhance' Checkbox
				"Disabled",	# 'Input Image: Upscale or Variation:' Radio
				"Before First Enhancement",	# 'Enhance: Order of Processing'
				"Original Prompts",	# 'Enhance: Prompt' Radio
                # Enhance #1
				False,	# 'Enable' Checkbox
				"",		# 'Detection prompt' Textbox
				"",		# 'Enhancement positive prompt' Textbox
				"",		# 'Enhancement negative prompt' Textbox
				"sam",	# 'Mask generation model'
				"full",	# 'u2net_cloth: Cloth category' Dropdown
				"vit_b",# 'SAM model' Dropdown
				0.25,	# [0, 1.0] in 'Text Threshold'
				0.3,	# [0, 1.0] in 'Box Threshold' Slider
				0,		# [0, 10] in 'Maximum number of detections'
				True,	# bool in 'Disable initial latent in inpaint'
                # Enhance/Inpaint
				"v2.6",	# 'Inpaint Engine'
				1,		# [0, 1.0] in 'Inpaint Denoising Strength'
				0.618,	# [0, 1.0] in 'Inpaint Respective Field'
				0,		# [-64, 64] in 'Mask Erode or Dilate'
				False,	# 'Invert Mask' Checkbox
                # Enhance #2
				False,	# 'Enable' Checkbox
				"",		# 'Detection prompt' Textbox
				"",		# 'Enhancement positive prompt' Textbox
				"",		# 'Enhancement negative prompt' Textbox
				"sam",	# 'Mask generation model'
				"full",	# 'u2net_cloth: Cloth category' Dropdown
				"vit_b",# 'SAM model' Dropdown
				0.25,	# [0, 1.0] in 'Text Threshold'
				0.3,	# [0, 1.0] in 'Box Threshold' Slider
				0,		# [0, 10] in 'Maximum number of detections'
				True,	# bool in 'Disable initial latent in inpaint'
                # Enhance/Inpaint
				"v2.6",	# 'Inpaint Engine'
				1,		# [0, 1.0] in 'Inpaint Denoising Strength'
				0.618,	# [0, 1.0] in 'Inpaint Respective Field'
				0,		# [-64, 64] in 'Mask Erode or Dilate'
				False,	# 'Invert Mask' Checkbox
                # Enhance #3
				False,	# 'Enable' Checkbox
				"",		# 'Detection prompt' Textbox
				"",		# 'Enhancement positive prompt' Textbox
				"",		# 'Enhancement negative prompt' Textbox
				"sam",	# 'Mask generation model'
				"full",	# 'u2net_cloth: Cloth category' Dropdown
				"vit_b",# 'SAM model' Dropdown
				0.25,	# [0, 1.0] in 'Text Threshold'
				0.3,	# [0, 1.0] in 'Box Threshold' Slider
				0,		# [0, 10] in 'Maximum number of detections'
				True,	# bool in 'Disable initial latent in inpaint'
                # Enhance/Inpaint
				"v2.6",	# 'Inpaint Engine'
				1,		# [0, 1.0] in 'Inpaint Denoising Strength'
				0.618,	# [0, 1.0] in 'Inpaint Respective Field'
				0,		# [-64, 64] in 'Mask Erode or Dilate'
				False,	# 'Invert Mask' Checkbox
				fn_index=67
)
            
            # Второй вызов API
            result = client.predict(fn_index=68)
            
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
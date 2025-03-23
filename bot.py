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
        'Привет Я бот для генерации изображений через Fooocus. '
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
        
        print("\n=== First predict call ===")
        print("Prompt:", prompt)
        print("Seed:", seed)
        
        # Запускаем генерацию (fn_index=67)
        job = client.predict(
				True,	# bool # in 'Generate Image Grid for Each Batch' Checkbox component
				prompt,	# str # in 'parameter_12' Textbox component
				"Howdy!",	# str # in 'Negative Prompt' Textbox component
				["Fooocus V2"],	# List[str] # in 'Selected Styles' Checkboxgroup component
				"Quality",	# str # in 'Performance' Radio component
				"704×1408 <span style="color: grey;"> ∣ 1:2</span>",	# str # in 'Aspect Ratios' Radio component
				1,	# int | float (numeric value between 1 and 32)
								# in 'Image Number' Slider component
				"png",	# str # in 'Output Format' Radio component
				"Howdy!",	# str # in 'Seed' Textbox component
				True,	# bool # in 'Read wildcards in order' Checkbox component
				0,	# int | float (numeric value between 0.0 and 30.0)
								# in 'Image Sharpness' Slider component
				1,	# int | float (numeric value between 1.0 and 30.0)
								# in 'Guidance Scale' Slider component
				"juggernautXL_v8Rundiffusion.safetensors",	# str (Option from: ['juggernautXL_v8Rundiffusion.safetensors'])
								# in 'Base Model (SDXL only)' Dropdown component
				"None",	# str (Option from: ['None', 'juggernautXL_v8Rundiffusion.safetensors'])
								# in 'Refiner (SDXL or SD 1.5)' Dropdown component
				0.1,	# int | float (numeric value between 0.1 and 1.0)
								# in 'Refiner Switch At' Slider component
				True,	# bool # in 'Enable' Checkbox component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors'])
								# in 'LoRA 1' Dropdown component
				-2,	# int | float (numeric value between -2 and 2)
								# in 'Weight' Slider component
				True,	# bool # in 'Enable' Checkbox component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors'])
								# in 'LoRA 2' Dropdown component
				-2,	# int | float (numeric value between -2 and 2)
								# in 'Weight' Slider component
				True,	# bool # in 'Enable' Checkbox component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors'])
								# in 'LoRA 3' Dropdown component
				-2,	# int | float (numeric value between -2 and 2)
								# in 'Weight' Slider component
				True,	# bool # in 'Enable' Checkbox component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors'])
								# in 'LoRA 4' Dropdown component
				-2,	# int | float (numeric value between -2 and 2)
								# in 'Weight' Slider component
				True,	# bool # in 'Enable' Checkbox component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors'])
								# in 'LoRA 5' Dropdown component
				-2,	# int | float (numeric value between -2 and 2)
								# in 'Weight' Slider component
				True,	# bool # in 'Input Image' Checkbox component
				"Howdy!",	# str # in 'parameter_212' Textbox component
				"Disabled",	# str # in 'Upscale or Variation:' Radio component
				"https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",	# str (filepath or URL to image)
								# in 'Image' Image component
				["Left"],	# List[str] # in 'Outpaint Direction' Checkboxgroup component
				"https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",	# str (filepath or URL to image)
								# in 'Image' Image component
				"Howdy!",	# str # in 'Inpaint Additional Prompt' Textbox component
				"https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",	# str (filepath or URL to image)
								# in 'Mask Upload' Image component
				True,	# bool # in 'Disable Preview' Checkbox component
				True,	# bool # in 'Disable Intermediate Results' Checkbox component
				True,	# bool # in 'Disable seed increment' Checkbox component
				True,	# bool # in 'Black Out NSFW' Checkbox component
				0.1,	# int | float (numeric value between 0.1 and 3.0)
								# in 'Positive ADM Guidance Scaler' Slider component
				0.1,	# int | float (numeric value between 0.1 and 3.0)
								# in 'Negative ADM Guidance Scaler' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'ADM Guidance End At Step' Slider component
				1,	# int | float (numeric value between 1.0 and 30.0)
								# in 'CFG Mimicking from TSNR' Slider component
				1,	# int | float (numeric value between 1 and 12)
								# in 'CLIP Skip' Slider component
				"euler",	# str (Option from: ['euler', 'euler_ancestral', 'heun', 'heunpp2', 'dpm_2', 'dpm_2_ancestral', 'lms', 'dpm_fast', 'dpm_adaptive', 'dpmpp_2s_ancestral', 'dpmpp_sde', 'dpmpp_sde_gpu', 'dpmpp_2m', 'dpmpp_2m_sde', 'dpmpp_2m_sde_gpu', 'dpmpp_3m_sde', 'dpmpp_3m_sde_gpu', 'ddpm', 'lcm', 'tcd', 'restart', 'ddim', 'uni_pc', 'uni_pc_bh2'])
								# in 'Sampler' Dropdown component
				"normal",	# str (Option from: ['normal', 'karras', 'exponential', 'sgm_uniform', 'simple', 'ddim_uniform', 'lcm', 'turbo', 'align_your_steps', 'tcd', 'edm_playground_v2.5'])
								# in 'Scheduler' Dropdown component
				"Default (model)",	# str (Option from: ['Default (model)'])
								# in 'VAE' Dropdown component
				-1,	# int | float (numeric value between -1 and 200)
								# in 'Forced Overwrite of Sampling Step' Slider component
				-1,	# int | float (numeric value between -1 and 200)
								# in 'Forced Overwrite of Refiner Switch Step' Slider component
				-1,	# int | float (numeric value between -1 and 2048)
								# in 'Forced Overwrite of Generating Width' Slider component
				-1,	# int | float (numeric value between -1 and 2048)
								# in 'Forced Overwrite of Generating Height' Slider component
				-1,	# int | float (numeric value between -1 and 1.0)
								# in 'Forced Overwrite of Denoising Strength of "Vary"' Slider component
				-1,	# int | float (numeric value between -1 and 1.0)
								# in 'Forced Overwrite of Denoising Strength of "Upscale"' Slider component
				True,	# bool # in 'Mixing Image Prompt and Vary/Upscale' Checkbox component
				True,	# bool # in 'Mixing Image Prompt and Inpaint' Checkbox component
				True,	# bool # in 'Debug Preprocessors' Checkbox component
				True,	# bool # in 'Skip Preprocessors' Checkbox component
				1,	# int | float (numeric value between 1 and 255)
								# in 'Canny Low Threshold' Slider component
				1,	# int | float (numeric value between 1 and 255)
								# in 'Canny High Threshold' Slider component
				"joint",	# str (Option from: ['joint', 'separate', 'vae'])
								# in 'Refiner swap method' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Softness of ControlNet' Slider component
				True,	# bool # in 'Enabled' Checkbox component
				0,	# int | float (numeric value between 0 and 2)
								# in 'B1' Slider component
				0,	# int | float (numeric value between 0 and 2)
								# in 'B2' Slider component
				0,	# int | float (numeric value between 0 and 4)
								# in 'S1' Slider component
				0,	# int | float (numeric value between 0 and 4)
								# in 'S2' Slider component
				True,	# bool # in 'Debug Inpaint Preprocessing' Checkbox component
				True,	# bool # in 'Disable initial latent in inpaint' Checkbox component
				"None",	# str (Option from: ['None', 'v1', 'v2.5', 'v2.6'])
								# in 'Inpaint Engine' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Inpaint Denoising Strength' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Inpaint Respective Field' Slider component
				True,	# bool # in 'Enable Advanced Masking Features' Checkbox component
				True,	# bool # in 'Invert Mask When Generating' Checkbox component
				-64,	# int | float (numeric value between -64 and 64)
								# in 'Mask Erode or Dilate' Slider component
				True,	# bool # in 'Save only final enhanced image' Checkbox component
				True,	# bool # in 'Save Metadata to Images' Checkbox component
				"fooocus",	# str # in 'Metadata Scheme' Radio component
				"https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",	# str (filepath or URL to image)
								# in 'Image' Image component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Stop At' Slider component
				0,	# int | float (numeric value between 0.0 and 2.0)
								# in 'Weight' Slider component
				"ImagePrompt",	# str # in 'Type' Radio component
				"https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",	# str (filepath or URL to image)
								# in 'Image' Image component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Stop At' Slider component
				0,	# int | float (numeric value between 0.0 and 2.0)
								# in 'Weight' Slider component
				"ImagePrompt",	# str # in 'Type' Radio component
				"https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",	# str (filepath or URL to image)
								# in 'Image' Image component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Stop At' Slider component
				0,	# int | float (numeric value between 0.0 and 2.0)
								# in 'Weight' Slider component
				"ImagePrompt",	# str # in 'Type' Radio component
				"https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",	# str (filepath or URL to image)
								# in 'Image' Image component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Stop At' Slider component
				0,	# int | float (numeric value between 0.0 and 2.0)
								# in 'Weight' Slider component
				"ImagePrompt",	# str # in 'Type' Radio component
				True,	# bool # in 'Debug GroundingDINO' Checkbox component
				-64,	# int | float (numeric value between -64 and 64)
								# in 'GroundingDINO Box Erode or Dilate' Slider component
				True,	# bool # in 'Debug Enhance Masks' Checkbox component
				"https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",	# str (filepath or URL to image)
								# in 'Use with Enhance, skips image generation' Image component
				True,	# bool # in 'Enhance' Checkbox component
				"Disabled",	# str # in 'Upscale or Variation:' Radio component
				"Before First Enhancement",	# str # in 'Order of Processing' Radio component
				"Original Prompts",	# str # in 'Prompt' Radio component
				True,	# bool # in 'Enable' Checkbox component
				"Howdy!",	# str # in 'Detection prompt' Textbox component
				"Howdy!",	# str # in 'Enhancement positive prompt' Textbox component
				"Howdy!",	# str # in 'Enhancement negative prompt' Textbox component
				"u2net",	# str (Option from: ['u2net', 'u2netp', 'u2net_human_seg', 'u2net_cloth_seg', 'silueta', 'isnet-general-use', 'isnet-anime', 'sam'])
								# in 'Mask generation model' Dropdown component
				"full",	# str (Option from: ['full', 'upper', 'lower'])
								# in 'Cloth category' Dropdown component
				"vit_b",	# str (Option from: ['vit_b', 'vit_l', 'vit_h'])
								# in 'SAM model' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Text Threshold' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Box Threshold' Slider component
				0,	# int | float (numeric value between 0 and 10)
								# in 'Maximum number of detections' Slider component
				True,	# bool # in 'Disable initial latent in inpaint' Checkbox component
				"None",	# str (Option from: ['None', 'v1', 'v2.5', 'v2.6'])
								# in 'Inpaint Engine' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Inpaint Denoising Strength' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Inpaint Respective Field' Slider component
				-64,	# int | float (numeric value between -64 and 64)
								# in 'Mask Erode or Dilate' Slider component
				True,	# bool # in 'Invert Mask' Checkbox component
				True,	# bool # in 'Enable' Checkbox component
				"Howdy!",	# str # in 'Detection prompt' Textbox component
				"Howdy!",	# str # in 'Enhancement positive prompt' Textbox component
				"Howdy!",	# str # in 'Enhancement negative prompt' Textbox component
				"u2net",	# str (Option from: ['u2net', 'u2netp', 'u2net_human_seg', 'u2net_cloth_seg', 'silueta', 'isnet-general-use', 'isnet-anime', 'sam'])
								# in 'Mask generation model' Dropdown component
				"full",	# str (Option from: ['full', 'upper', 'lower'])
								# in 'Cloth category' Dropdown component
				"vit_b",	# str (Option from: ['vit_b', 'vit_l', 'vit_h'])
								# in 'SAM model' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Text Threshold' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Box Threshold' Slider component
				0,	# int | float (numeric value between 0 and 10)
								# in 'Maximum number of detections' Slider component
				True,	# bool # in 'Disable initial latent in inpaint' Checkbox component
				"None",	# str (Option from: ['None', 'v1', 'v2.5', 'v2.6'])
								# in 'Inpaint Engine' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Inpaint Denoising Strength' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Inpaint Respective Field' Slider component
				-64,	# int | float (numeric value between -64 and 64)
								# in 'Mask Erode or Dilate' Slider component
				True,	# bool # in 'Invert Mask' Checkbox component
				True,	# bool # in 'Enable' Checkbox component
				"Howdy!",	# str # in 'Detection prompt' Textbox component
				"Howdy!",	# str # in 'Enhancement positive prompt' Textbox component
				"Howdy!",	# str # in 'Enhancement negative prompt' Textbox component
				"u2net",	# str (Option from: ['u2net', 'u2netp', 'u2net_human_seg', 'u2net_cloth_seg', 'silueta', 'isnet-general-use', 'isnet-anime', 'sam'])
								# in 'Mask generation model' Dropdown component
				"full",	# str (Option from: ['full', 'upper', 'lower'])
								# in 'Cloth category' Dropdown component
				"vit_b",	# str (Option from: ['vit_b', 'vit_l', 'vit_h'])
								# in 'SAM model' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Text Threshold' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Box Threshold' Slider component
				0,	# int | float (numeric value between 0 and 10)
								# in 'Maximum number of detections' Slider component
				True,	# bool # in 'Disable initial latent in inpaint' Checkbox component
				"None",	# str (Option from: ['None', 'v1', 'v2.5', 'v2.6'])
								# in 'Inpaint Engine' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Inpaint Denoising Strength' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								# in 'Inpaint Respective Field' Slider component
				-64,	# int | float (numeric value between -64 and 64)
								# in 'Mask Erode or Dilate' Slider component
				True,	# bool # in 'Invert Mask' Checkbox component
				fn_index=67
        )
        
        print("Job type:", type(job))
        print("Job:", job)
        print("================\n")
        
        # Получаем результат
        result = client.predict(fn_index=68)
        print("\n=== Second predict call ===")
        print("Type:", type(result))
        print("Result:", result)
        print("================\n")
        
        await update.message.reply_text('Изображение сгенерировано. Проверьте консоль для просмотра результата.')
            
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
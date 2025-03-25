import os
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context):
    await update.message.reply_text('Привет! Отправь мне текстовый запрос, и я сгенерирую для тебя изображение.')

async def generate_image(update: Update, context):
    user_prompt = update.message.text
    await update.message.reply_text('🔄 Начинаю генерацию изображения...')
    
    try:
        image_url = await fooocus_api_call(user_prompt)
        
        if image_url:
            await update.message.reply_photo(image_url)
        else:
            await update.message.reply_text('❌ Не удалось сгенерировать изображение')
            
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        await update.message.reply_text('⚠️ Произошла ошибка при генерации изображения')

async def fooocus_api_call(prompt: str) -> str:
    API_URL = os.getenv('API_URL')
    
    payload = {
        "fn_index": 67,
        "data": [
                True, "", prompt, ["Fooocus V2"],
                "Hyper-SD", "1152×896", 1, "png", "", True,
                2, 4, "juggernautXL_v8Rundiffusion.safetensors",
                "None", 0.1,
                True, "sd_xl_offset_example-lora_1.0.safetensors", 0.1,
                True, "None", 1,
                True, "None", 1,
                True, "None", 1,
                True, "None", 1,
                True, "",  # Добавлен недостающий параметр
                "Disabled", "", [],
                "", "", "",
                "", 0.9, 0.75, "FaceSwap",
                "", 0, 0, "ImagePrompt",
                "", 0, 0, "ImagePrompt",
                "", 0, 0, "ImagePrompt",
                True, -64, True, "",
                True, "Disabled", "Before First Enhancement",
                "Original Prompts", True, "Howdy!", "Howdy!", "Howdy!",
                "u2net", "full", "vit_b", 0, 0, 0,
                True, "None", 0, 0, -64, True,
                True, "Howdy!", "Howdy!", "Howdy!", "u2net",
                "full", "vit_b", 0, 0, 0, True,
                "None", 0, 0, -64, True,
                True, "Howdy!", "Howdy!", "Howdy!", "u2net",
                "full", "vit_b", 0, 0, 0,
                True, "None", 0, 0, -64, True
        ]
    }
    
    try:
        response = requests.post(f"{API_URL}", json=payload)
        response.raise_for_status()
        result = response.json()
        
        if 'data' in result and len(result['data']) > 0:
            return result['data'][0]
            
    except Exception as e:
        logging.error(f"API Error: {str(e)}")
        return None

def main():
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    
    application.run_polling()

if __name__ == '__main__':
    main()
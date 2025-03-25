import os
import time
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from gradio_client import Client

TOKEN = os.getenv('TELEGRAM_TOKEN')
API_URL = "http://192.168.252.100:7865/"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context):
    await update.message.reply_text('🎨 Привет! Отправь промпт для генерации изображения.')

async def handle_message(update: Update, context):
    try:
        prompt = update.message.text
        client = Client(API_URL)
        
        # Шаг 1: Запуск генерации
        await update.message.reply_text('⚙️ Запускаю генерацию...')
        job = client.predict(
            True, prompt, "", ["Fooocus V2"], 
            "Quality", "704×1408", 1, "png", "", True,
            0, 1.5, "juggernautXL_v8Rundiffusion.safetensors",
            "None", 0.1, True, "None", -2, True, "None", -2,
            True, "None", -2, True, "None", -2, True, "None", -2,
            True, "", "Disabled", "", [], "", "", "",
            True, True, False, False, 1.5, 0.8, 0.3, 7, 2,
            "dpmpp_2m_sde_gpu", "karras", "Default (model)",
            -1, -1, -1, -1, -1, -1, True, True, False, False,
            64, 128, "joint", 0.25, False, 0, 0, 0, 0,
            False, False, "v2.6", 1.0, 0.618, False, False, 6,
            False, "fooocus", "", 0, 0, "ImagePrompt", "", 0, 0, "ImagePrompt",
            "", 0, 0, "ImagePrompt", "", 0, 0, "ImagePrompt",
            True, -64, True, "", True, "Disabled", "Before First Enhancement",
            "Original Prompts", True, "person", "high quality", "low quality",
            "u2net", "full", "vit_b", 0.7, 0.3, 10, True, "None", 1.0, 0.618, -64, True,
            True, "person", "high quality", "low quality", "u2net", "full", "vit_b",
            0.7, 0.3, 10, True, "None", 1.0, 0.618, -64, True,
            True, "person", "high quality", "low quality", "u2net", "full", "vit_b",
            0.7, 0.3, 10, True, "None", 1.0, 0.618, -64, True,
            fn_index=67
        )
        
        # Ожидание завершения генерации
#        while not job.done():
#            time.sleep(2)
#            await update.message.reply_text('⏳ Обрабатываю запрос...')
        
        # Шаг 2: Получение результатов
        await update.message.reply_text('🔍 Получаю результат...')
        result = client.predict(fn_index=68)
        
        # Извлечение URL изображения
        if result and len(result) > 2:
            gallery = result[2]
            if isinstance(gallery, list) and len(gallery) > 0:
                image_url = gallery[0]['url']
                await update.message.reply_photo(image_url)
                return
                
        await update.message.reply_text('❌ Не удалось получить изображение')

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        await update.message.reply_text('⚠️ Произошла ошибка при обработке запроса')

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
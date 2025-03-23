import os
import logging
import asyncio
from io import BytesIO
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from gradio_client import Client

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_URL = os.getenv('FOOOCUS_API_URL', 'http://localhost:7860')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎨 Отправьте текстовый запрос для генерации изображения")

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    if not prompt:
        await update.message.reply_text("❌ Пожалуйста, введите текстовый запрос")
        return

    try:
        msg = await update.message.reply_text("🔄 Начинаю генерацию...")
        
        client = Client(API_URL)
        
        # Запуск генерации через fn_index=67
        job = client.submit(
            True,                # Generate Image Grid
            prompt,              # Основной промпт
            "",                  # Негативный промпт
            ["Fooocus V2"],      # Стили
            "Quality",           # Производительность
            "704×1408",         # Соотношение сторон
            1,                   # Количество изображений
            "png",               # Формат вывода
            "Random",            # Сид
            True,                # Читать wildcards по порядку
            0,                   # Резкость изображения
            7.5,                 # Шкала классификатора
            "juggernautXL_v8Rundiffusion.safetensors",  # Базовая модель
            "None",              # Уточняющая модель
            0.5,                 # Переключение уточняющей модели
            True, False, "None", -2,  # LoRA 1
            True, False, "None", -2,  # LoRA 2
            True, False, "None", -2,  # LoRA 3
            True, False, "None", -2,  # LoRA 4
            True, False, "None", -2,  # LoRA 5
            False, "", "Disabled", None, [], None, "", None, False, False, False, False,
            0.1, 0.1, 0, 1, 1, "euler", "normal", "Default (model)", -1, -1, -1, -1, -1, -1,
            True, True, False, False, 100, 200, "joint", 0, True, 0, 0, 0, 0, False, False,
            "None", 0, 0, True, False, -64, True, True, "fooocus", None, 0, 0, "ImagePrompt",
            None, 0, 0, "ImagePrompt", None, 0, 0, "ImagePrompt", None, 0, 0, "ImagePrompt",
            False, -64, False, None, True, "Disabled", "Before First Enhancement",
            "Original Prompts", True, "", "", "", "u2net", "full", "vit_b", 0, 0, 0, False,
            "None", 0, 0, -64, True, True, "", "", "", "u2net", "full", "vit_b", 0, 0, 0, False,
            "None", 0, 0, -64, True, True, "", "", "", "u2net", "full", "vit_b", 0, 0, 0, False,
            "None", 0, 0, -64, True,
            fn_index=67
        )

        # Ожидание завершения генерации
        while not job.done():
            await asyncio.sleep(5)
            await msg.edit_text("⏳ Генерация в процессе...")

        # Получение результатов через fn_index=68
        result = client.predict(fn_index=68)
        
        if result and len(result) > 2:
            image_url = result[2][0]['url']  # Предполагаем, что изображение в третьем элементе
            response = requests.get(image_url)
            
            bio = BytesIO(response.content)
            bio.name = 'generated_image.png'
            bio.seek(0)
            
            await msg.delete()
            await update.message.reply_photo(photo=bio)
        else:
            await update.message.reply_text("⚠️ Не удалось получить изображение")

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        await update.message.reply_text("🔥 Произошла ошибка при генерации")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    app.run_polling()

if __name__ == "__main__":
    main()
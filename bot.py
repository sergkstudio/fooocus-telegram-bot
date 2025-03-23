import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Конфигурация
API_URL = "https://5e0bd9bbaf0cd0a9f7.gradio.live"  # Замените на ваш URL API
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Замените на токен вашего бота

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для генерации изображений.\n"
        "Просто отправь мне текстовое описание того, что ты хочешь увидеть."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text("🔄 Начинаю генерацию изображения...")
    
    try:
        image_url = generate_image(prompt)
        if image_url:
            await update.message.reply_photo(image_url)
        else:
            await update.message.reply_text("❌ Не удалось сгенерировать изображение")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

def generate_image(prompt: str) -> str:
    # Формируем payload для первого запроса
    payload = {
        "fn_index": 67,
        "data": [
            True,   # Generate Image Grid
            prompt, # Prompt
            "",     # Negative Prompt
            ["Fooocus V2"],  # Styles
            "Hyper-SD",      # Performance
            "1152×896",      # Aspect Ratio
            1,      # Image Number
            "png",  # Output Format
            "",     # Seed
            True,   # Read wildcards
            
            # Advanced Settings
            2,      # Sharpness
            4,      # Guidance Scale
            "juggernautXL_v8Rundiffusion.safetensors",  # Base Model
            "None", # Refiner
            0.1,    # Refiner Switch
            True, "sd_xl_offset_example-lora_1.0.safetensors", 0.1,  # LoRA 1
            True, "None", 1,  # LoRA 2
            True, "None", 1,  # LoRA 3
            True, "None", 1,  # LoRA 4
            True, "None", 1,  # LoRA 5
            
            # Input Image (отключено)
            False,  # Input Image Checkbox
            "",     # parameter_95
            
            # Upscale/Variation
            "Disabled", "", [],
            
            # Inpaint/Outpaint (пустые значения)
            "", "", "",
            
            # Advanced Developer Settings
            True, True, False, False,  # Disable options
            1.5, 0.8, 0.3, 7, 2,       # ADM Guidance
            "dpmpp_2m_sde_gpu", "karras", "Default (model)",  # Sampler
            -1, -1, -1, -1, -1, -1,    # Overwrites
            False, True, False, False, 64, 128, "joint", 0.25,  # ControlNet
            False, 0, 0, 0, 0,         # FreeU
            False, False, "v2.6", 1, 0.618, False, False, 6, False, "fooocus",  # Inpaint
            
            # Image Prompts (отключены)
            "", 0, 0, "ImagePrompt",    # Image Prompt 1
            "", 0, 0, "ImagePrompt",    # Image Prompt 2
            "", 0, 0, "ImagePrompt",    # Image Prompt 3
            "", 0, 0, "ImagePrompt",    # Image Prompt 4
            
            # Остальные параметры
            True, -64, True, "", True, "Disabled", "Before First Enhancement",
            "Original Prompts", True, "", "", "", "u2net", "full", "vit_b",
            0, 0, 0, True, "None", 0, 0, -64, True,
            True, "", "", "", "u2net", "full", "vit_b", 0, 0, 0, True,
            "None", 0, 0, -64, True, True, "", "", "", "u2net",
            "full", "vit_b", 0, 0, 0, True, "None", 0, 0, -64, True
        ]
    }

    # Первый запрос
    response = requests.post(f"{API_URL}/api/predict", json=payload)
    response.raise_for_status()
    
    # Второй запрос для получения результата
    response = requests.post(
        f"{API_URL}/api/predict",
        json={"fn_index": 68, "data": []}
    )
    response.raise_for_status()
    
    return response.json()[2]

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен...")
    app.run_polling()
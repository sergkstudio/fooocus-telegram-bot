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

# Выводим список доступных эндпоинтов при запуске
logger.info("Доступные эндпоинты:")
try:
    # Получаем список всех доступных эндпоинтов
    endpoints = client.endpoints
    for endpoint_name in endpoints:
        logger.info(f"- {endpoint_name}")
except Exception as e:
    logger.error(f"Ошибка при получении списка эндпоинтов: {str(e)}")

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
            # Запускаем генерацию изображения через Gradio API
            result = client.predict(
                prompt,  # текстовый промпт
                "Quality",  # производительность
                "704×1408",  # соотношение сторон
                1,  # количество изображений
                "png",  # формат вывода
                "",  # seed (пустой для случайного)
                True,  # read wildcards in order
                0,  # sharpness
                1,  # guidance scale
                "juggernautXL_v8Rundiffusion.safetensors",  # базовая модель
                "None",  # refiner
                0.1,  # refiner switch at
                True,  # enable LoRA 1
                "None",  # LoRA 1
                -2,  # weight LoRA 1
                True,  # enable LoRA 2
                "None",  # LoRA 2
                -2,  # weight LoRA 2
                True,  # enable LoRA 3
                "None",  # LoRA 3
                -2,  # weight LoRA 3
                True,  # enable LoRA 4
                "None",  # LoRA 4
                -2,  # weight LoRA 4
                True,  # enable LoRA 5
                "None",  # LoRA 5
                -2,  # weight LoRA 5
                False,  # input image
                "",  # parameter_212
                "Disabled",  # upscale or variation
                None,  # image
                [],  # outpaint direction
                None,  # image
                "",  # inpaint additional prompt
                None,  # mask upload
                False,  # disable preview
                False,  # disable intermediate results
                False,  # disable seed increment
                False,  # black out nsfw
                0.1,  # positive adm guidance scaler
                0.1,  # negative adm guidance scaler
                0,  # adm guidance end at step
                1,  # cfg mimicking from tsnr
                1,  # clip skip
                "euler",  # sampler
                "normal",  # scheduler
                "Default (model)",  # vae
                -1,  # forced overwrite of sampling step
                -1,  # forced overwrite of refiner switch step
                -1,  # forced overwrite of generating width
                -1,  # forced overwrite of generating height
                -1,  # forced overwrite of denoising strength of vary
                -1,  # forced overwrite of denoising strength of upscale
                True,  # mixing image prompt and vary/upscale
                True,  # mixing image prompt and inpaint
                False,  # debug preprocessors
                False,  # skip preprocessors
                1,  # canny low threshold
                1,  # canny high threshold
                "joint",  # refiner swap method
                0,  # softness of controlnet
                True,  # enabled
                0,  # b1
                0,  # b2
                0,  # s1
                0,  # s2
                False,  # debug inpaint preprocessing
                False,  # disable initial latent in inpaint
                "None",  # inpaint engine
                0,  # inpaint denoising strength
                0,  # inpaint respective field
                False,  # enable advanced masking features
                False,  # invert mask when generating
                -64,  # mask erode or dilate
                False,  # save only final enhanced image
                False,  # save metadata to images
                "fooocus",  # metadata scheme
                None,  # image
                0,  # stop at
                0,  # weight
                "ImagePrompt",  # type
                None,  # image
                0,  # stop at
                0,  # weight
                "ImagePrompt",  # type
                None,  # image
                0,  # stop at
                0,  # weight
                "ImagePrompt",  # type
                None,  # image
                0,  # stop at
                0,  # weight
                "ImagePrompt",  # type
                False,  # debug groundingdino
                -64,  # groundingdino box erode or dilate
                False,  # debug enhance masks
                None,  # use with enhance, skips image generation
                False,  # enhance
                "Disabled",  # upscale or variation
                "Before First Enhancement",  # order of processing
                "Original Prompts",  # prompt
                False,  # enable
                "",  # detection prompt
                "",  # enhancement positive prompt
                "",  # enhancement negative prompt
                "u2net",  # mask generation model
                "full",  # cloth category
                "vit_b",  # sam model
                0,  # text threshold
                0,  # box threshold
                0,  # maximum number of detections
                False,  # disable initial latent in inpaint
                "None",  # inpaint engine
                0,  # inpaint denoising strength
                0,  # inpaint respective field
                -64,  # mask erode or dilate
                False,  # invert mask
                False,  # enable
                "",  # detection prompt
                "",  # enhancement positive prompt
                "",  # enhancement negative prompt
                "u2net",  # mask generation model
                "full",  # cloth category
                "vit_b",  # sam model
                0,  # text threshold
                0,  # box threshold
                0,  # maximum number of detections
                False,  # disable initial latent in inpaint
                "None",  # inpaint engine
                0,  # inpaint denoising strength
                0,  # inpaint respective field
                -64,  # mask erode or dilate
                False,  # invert mask
                False,  # enable
                "",  # detection prompt
                "",  # enhancement positive prompt
                "",  # enhancement negative prompt
                "u2net",  # mask generation model
                "full",  # cloth category
                "vit_b",  # sam model
                0,  # text threshold
                0,  # box threshold
                0,  # maximum number of detections
                False,  # disable initial latent in inpaint
                "None",  # inpaint engine
                0,  # inpaint denoising strength
                0,  # inpaint respective field
                -64,  # mask erode or dilate
                False,  # invert mask
                False,  # enable
                "",  # detection prompt
                "",  # enhancement positive prompt
                "",  # enhancement negative prompt
                "u2net",  # mask generation model
                "full",  # cloth category
                "vit_b",  # sam model
                0,  # text threshold
                0,  # box threshold
                0,  # maximum number of detections
                False,  # disable initial latent in inpaint
                "None",  # inpaint engine
                0,  # inpaint denoising strength
                0,  # inpaint respective field
                -64,  # mask erode or dilate
                False,  # invert mask
                fn_index=67  # индекс функции для генерации изображения
            )
            
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
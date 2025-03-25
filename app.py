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
                True,	# bool #Generate Image Grid for Each Batch' Checkbox component
				prompt,	# str #parameter_12' Textbox component
				"",	# str #Negative Prompt' Textbox component
				["Fooocus V2"],	# List[str] #Selected Styles' Checkboxgroup component
				"Quality",	# str #Performance' Radio component
				"704×1408 <span style="color: grey;"> ∣ 1:2</span>",	# str #Aspect Ratios' Radio component
				1,	# int | float (numeric value between 1 and 32)
								#Image Number' Slider component
				"png",	# str #Output Format' Radio component
				"",	# str #Seed' Textbox component
				True,	# bool #Read wildcards in order' Checkbox component
				0,	# int | float (numeric value between 0.0 and 30.0)
								#Image Sharpness' Slider component
				1,	# int | float (numeric value between 1.0 and 30.0)
								#Guidance Scale' Slider component
				"juggernautXL_v8Rundiffusion.safetensors",	# str (Option from: ['juggernautXL_v8Rundiffusion.safetensors'])
								#Base Model (SDXL only)' Dropdown component
				"None",	# str (Option from: ['None', 'juggernautXL_v8Rundiffusion.safetensors'])
								#Refiner (SDXL or SD 1.5)' Dropdown component
				0.1,	# int | float (numeric value between 0.1 and 1.0)
								#Refiner Switch At' Slider component
				True,	# bool #Enable' Checkbox component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors', 'sdxl_hyper_sd_4step_lora.safetensors'])
								#LoRA 1' Dropdown component
				-2,	# int | float (numeric value between -2 and 2)
								#Weight' Slider component
				True,	# bool #Enable' Checkbox component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors', 'sdxl_hyper_sd_4step_lora.safetensors'])
								#LoRA 2' Dropdown component
				-2,	# int | float (numeric value between -2 and 2)
								#Weight' Slider component
				True,	# bool #Enable' Checkbox component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors', 'sdxl_hyper_sd_4step_lora.safetensors'])
								#LoRA 3' Dropdown component
				-2,	# int | float (numeric value between -2 and 2)
								#Weight' Slider component
				True,	# bool #Enable' Checkbox component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors', 'sdxl_hyper_sd_4step_lora.safetensors'])
								#LoRA 4' Dropdown component
				-2,	# int | float (numeric value between -2 and 2)
								#Weight' Slider component
				True,	# bool #Enable' Checkbox component
				"None",	# str (Option from: ['None', 'sd_xl_offset_example-lora_1.0.safetensors', 'sdxl_hyper_sd_4step_lora.safetensors'])
								#LoRA 5' Dropdown component
				-2,	# int | float (numeric value between -2 and 2)
								#Weight' Slider component
				True,	# bool #Input Image' Checkbox component
				"",	# str #parameter_212' Textbox component
				"Disabled",	# str #Upscale or Variation:' Radio component
				"",	# str (filepath or URL to image)
								#Image' Image component
				["Left"],	# List[str] #Outpaint Direction' Checkboxgroup component
				"",	# str (filepath or URL to image)
								#Image' Image component
				"",	# str #Inpaint Additional Prompt' Textbox component
				"",	# str (filepath or URL to image)
								#Mask Upload' Image component
				True,	# bool #Disable Preview' Checkbox component
				True,	# bool #Disable Intermediate Results' Checkbox component
				True,	# bool #Disable seed increment' Checkbox component
				True,	# bool #Black Out NSFW' Checkbox component
				0.1,	# int | float (numeric value between 0.1 and 3.0)
								#Positive ADM Guidance Scaler' Slider component
				0.1,	# int | float (numeric value between 0.1 and 3.0)
								#Negative ADM Guidance Scaler' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#ADM Guidance End At Step' Slider component
				1,	# int | float (numeric value between 1.0 and 30.0)
								#CFG Mimicking from TSNR' Slider component
				1,	# int | float (numeric value between 1 and 12)
								#CLIP Skip' Slider component
				"euler",	# str (Option from: ['euler', 'euler_ancestral', 'heun', 'heunpp2', 'dpm_2', 'dpm_2_ancestral', 'lms', 'dpm_fast', 'dpm_adaptive', 'dpmpp_2s_ancestral', 'dpmpp_sde', 'dpmpp_sde_gpu', 'dpmpp_2m', 'dpmpp_2m_sde', 'dpmpp_2m_sde_gpu', 'dpmpp_3m_sde', 'dpmpp_3m_sde_gpu', 'ddpm', 'lcm', 'tcd', 'restart', 'ddim', 'uni_pc', 'uni_pc_bh2'])
								#Sampler' Dropdown component
				"normal",	# str (Option from: ['normal', 'karras', 'exponential', 'sgm_uniform', 'simple', 'ddim_uniform', 'lcm', 'turbo', 'align_your_steps', 'tcd', 'edm_playground_v2.5'])
								#Scheduler' Dropdown component
				"Default (model)",	# str (Option from: ['Default (model)'])
								#VAE' Dropdown component
				-1,	# int | float (numeric value between -1 and 200)
								#Forced Overwrite of Sampling Step' Slider component
				-1,	# int | float (numeric value between -1 and 200)
								#Forced Overwrite of Refiner Switch Step' Slider component
				-1,	# int | float (numeric value between -1 and 2048)
								#Forced Overwrite of Generating Width' Slider component
				-1,	# int | float (numeric value between -1 and 2048)
								#Forced Overwrite of Generating Height' Slider component
				-1,	# int | float (numeric value between -1 and 1.0)
								#Forced Overwrite of Denoising Strength of "Vary"' Slider component
				-1,	# int | float (numeric value between -1 and 1.0)
								#Forced Overwrite of Denoising Strength of "Upscale"' Slider component
				True,	# bool #Mixing Image Prompt and Vary/Upscale' Checkbox component
				True,	# bool #Mixing Image Prompt and Inpaint' Checkbox component
				True,	# bool #Debug Preprocessors' Checkbox component
				True,	# bool #Skip Preprocessors' Checkbox component
				1,	# int | float (numeric value between 1 and 255)
								#Canny Low Threshold' Slider component
				1,	# int | float (numeric value between 1 and 255)
								#Canny High Threshold' Slider component
				"joint",	# str (Option from: ['joint', 'separate', 'vae'])
								#Refiner swap method' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Softness of ControlNet' Slider component
				True,	# bool #Enabled' Checkbox component
				0,	# int | float (numeric value between 0 and 2)
								#B1' Slider component
				0,	# int | float (numeric value between 0 and 2)
								#B2' Slider component
				0,	# int | float (numeric value between 0 and 4)
								#S1' Slider component
				0,	# int | float (numeric value between 0 and 4)
								#S2' Slider component
				True,	# bool #Debug Inpaint Preprocessing' Checkbox component
				True,	# bool #Disable initial latent in inpaint' Checkbox component
				"None",	# str (Option from: ['None', 'v1', 'v2.5', 'v2.6'])
								#Inpaint Engine' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Inpaint Denoising Strength' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Inpaint Respective Field' Slider component
				True,	# bool #Enable Advanced Masking Features' Checkbox component
				True,	# bool #Invert Mask When Generating' Checkbox component
				-64,	# int | float (numeric value between -64 and 64)
								#Mask Erode or Dilate' Slider component
				True,	# bool #Save only final enhanced image' Checkbox component
				True,	# bool #Save Metadata to Images' Checkbox component
				"fooocus",	# str #Metadata Scheme' Radio component
				"",	# str (filepath or URL to image)
								#Image' Image component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Stop At' Slider component
				0,	# int | float (numeric value between 0.0 and 2.0)
								#Weight' Slider component
				"ImagePrompt",	# str #Type' Radio component
				"",	# str (filepath or URL to image)
								#Image' Image component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Stop At' Slider component
				0,	# int | float (numeric value between 0.0 and 2.0)
								#Weight' Slider component
				"ImagePrompt",	# str #Type' Radio component
				"",	# str (filepath or URL to image)
								#Image' Image component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Stop At' Slider component
				0,	# int | float (numeric value between 0.0 and 2.0)
								#Weight' Slider component
				"ImagePrompt",	# str #Type' Radio component
				"",	# str (filepath or URL to image)
								#Image' Image component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Stop At' Slider component
				0,	# int | float (numeric value between 0.0 and 2.0)
								#Weight' Slider component
				"ImagePrompt",	# str #Type' Radio component
				True,	# bool #Debug GroundingDINO' Checkbox component
				-64,	# int | float (numeric value between -64 and 64)
								#GroundingDINO Box Erode or Dilate' Slider component
				True,	# bool #Debug Enhance Masks' Checkbox component
				"",	# str (filepath or URL to image)
								#Use with Enhance, skips image generation' Image component
				True,	# bool #Enhance' Checkbox component
				"Disabled",	# str #Upscale or Variation:' Radio component
				"Before First Enhancement",	# str #Order of Processing' Radio component
				"Original Prompts",	# str #Prompt' Radio component
				True,	# bool #Enable' Checkbox component
				"",	# str #Detection prompt' Textbox component
				"",	# str #Enhancement positive prompt' Textbox component
				"",	# str #Enhancement negative prompt' Textbox component
				"u2net",	# str (Option from: ['u2net', 'u2netp', 'u2net_human_seg', 'u2net_cloth_seg', 'silueta', 'isnet-general-use', 'isnet-anime', 'sam'])
								#Mask generation model' Dropdown component
				"full",	# str (Option from: ['full', 'upper', 'lower'])
								#Cloth category' Dropdown component
				"vit_b",	# str (Option from: ['vit_b', 'vit_l', 'vit_h'])
								#SAM model' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Text Threshold' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Box Threshold' Slider component
				0,	# int | float (numeric value between 0 and 10)
								#Maximum number of detections' Slider component
				True,	# bool #Disable initial latent in inpaint' Checkbox component
				"None",	# str (Option from: ['None', 'v1', 'v2.5', 'v2.6'])
								#Inpaint Engine' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Inpaint Denoising Strength' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Inpaint Respective Field' Slider component
				-64,	# int | float (numeric value between -64 and 64)
								#Mask Erode or Dilate' Slider component
				True,	# bool #Invert Mask' Checkbox component
				True,	# bool #Enable' Checkbox component
				"",	# str #Detection prompt' Textbox component
				"",	# str #Enhancement positive prompt' Textbox component
				"",	# str #Enhancement negative prompt' Textbox component
				"u2net",	# str (Option from: ['u2net', 'u2netp', 'u2net_human_seg', 'u2net_cloth_seg', 'silueta', 'isnet-general-use', 'isnet-anime', 'sam'])
								#Mask generation model' Dropdown component
				"full",	# str (Option from: ['full', 'upper', 'lower'])
								#Cloth category' Dropdown component
				"vit_b",	# str (Option from: ['vit_b', 'vit_l', 'vit_h'])
								#SAM model' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Text Threshold' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Box Threshold' Slider component
				0,	# int | float (numeric value between 0 and 10)
								#Maximum number of detections' Slider component
				True,	# bool #Disable initial latent in inpaint' Checkbox component
				"None",	# str (Option from: ['None', 'v1', 'v2.5', 'v2.6'])
								#Inpaint Engine' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Inpaint Denoising Strength' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Inpaint Respective Field' Slider component
				-64,	# int | float (numeric value between -64 and 64)
								#Mask Erode or Dilate' Slider component
				True,	# bool #Invert Mask' Checkbox component
				True,	# bool #Enable' Checkbox component
				"",	# str #Detection prompt' Textbox component
				"",	# str #Enhancement positive prompt' Textbox component
				"",	# str #Enhancement negative prompt' Textbox component
				"u2net",	# str (Option from: ['u2net', 'u2netp', 'u2net_human_seg', 'u2net_cloth_seg', 'silueta', 'isnet-general-use', 'isnet-anime', 'sam'])
								#Mask generation model' Dropdown component
				"full",	# str (Option from: ['full', 'upper', 'lower'])
								#Cloth category' Dropdown component
				"vit_b",	# str (Option from: ['vit_b', 'vit_l', 'vit_h'])
								#SAM model' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Text Threshold' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Box Threshold' Slider component
				0,	# int | float (numeric value between 0 and 10)
								#Maximum number of detections' Slider component
				True,	# bool #Disable initial latent in inpaint' Checkbox component
				"None",	# str (Option from: ['None', 'v1', 'v2.5', 'v2.6'])
								#Inpaint Engine' Dropdown component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Inpaint Denoising Strength' Slider component
				0,	# int | float (numeric value between 0.0 and 1.0)
								#Inpaint Respective Field' Slider component
				-64,	# int | float (numeric value between -64 and 64)
								#Mask Erode or Dilate' Slider component
				True,	# bool #Invert Mask' Checkbox component
        ]
    }
    
    try:
        response = requests.post(f"{API_URL}/api/predict", json=payload)
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
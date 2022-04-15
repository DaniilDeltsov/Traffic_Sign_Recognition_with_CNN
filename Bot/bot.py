from token_file import *
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
from model_predict import make_prediction
from aiogram.utils.executor import start_webhook

TOKEN = hidden_token
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

im1 = open("1.png", "rb")
im2 = open("2.png", "rb")

@dp.message_handler(commands=['start'])
async def send_welcome(msg: types.Message):
    await msg.reply(f"Привет, {msg.from_user.first_name}! \n"
                    f"Я бот, который умеет определять дорожные знаки по фото. \n"
                    f"Просто отправь мне картинку, и я скажу, что это за знак! \n"
                    f"К сожалению, я пока не умею самостоятельно находить знак на большой картинке, поэтому "
                    f"постарайся обрезать фото так, чтобы на нем было минимум фона, а знак был в центре. "
                    f"Если ты считаешь, что я ответил неправильно, то, пожалуйста, отправь фото еще раз "
                    f"КРУПНЫМ планом. \n\n"
                    f"Напиши /help, если нужна помощь или хочешь посмотреть, какие фото нужно отправлять.", reply=False)

@dp.message_handler(commands=['help'])
async def send_help(msg: types.Message):
    await msg.reply(f"Все просто! Отправь любой российский дорожный знак крупным планом. "
                    f"Я уже знаю целых 205 различных дорожных знаков!", reply=False)
    await msg.reply_photo(im1, "Например, вот так.", reply=False)
    await msg.reply_photo(im2, "Или так!", reply=False)

@dp.message_handler(content_types=['photo'])
async def predict_photo(msg):
    download_dir = './img/'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    img_name = 'img' + str(msg.from_user.id) + '.png'
    await msg.photo[-1].download('./img/' + img_name)
    answer = make_prediction('./img/' + img_name)
    os.remove('./img/' + img_name)
    await msg.reply(f"{answer}")

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()

if __name__ == '__main__':
    executor.start_polling(dp)

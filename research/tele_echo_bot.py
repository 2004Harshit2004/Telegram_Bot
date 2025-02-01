import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN= os.getenv('Telegram_bot_token')

# configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot=Bot(API_TOKEN)
dp=Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when client send `/start` or `/help` commands.
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
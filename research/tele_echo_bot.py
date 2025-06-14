# github.com/saikumar0605/telegram-bot
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
# Dispatcher: To send and receive messages between telegram bot and openai 'Dispatcher' is used as backend medium.
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
# load_dotenv: It is a library. It will used to read contents in .env file.
import os

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# configure logging
logging.basicConfig(level=logging.INFO)

# Initialize not and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# The following code is from: https://docs.aiogram.dev/en/latest/
@dp.message(Command(commands=["start", "help"]))
async def command_start_handler(message: Message):
    """
    This function/handler receives message with '/start' or '/help' command
    """
    # When '/start' command is given then following message will be printed by telegram bot which is 'qualcomm bot'.
    await message.reply("Hi\nI am Echo Bot!\nPowered by aiogram v3")

@dp.message(F.text) # Generic echo handler for any text
async def echo(message: Message):
    """
    This will return echo.
    """
    # This function will print or return whatever message we pass. 
    # If we pass 'Hi' the 'qualcomm bot' will print/return 'Hi'
    # If we pass 'Khanjan' the 'qualcomm bot' will print/return 'Khanjan'
    await message.answer(message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
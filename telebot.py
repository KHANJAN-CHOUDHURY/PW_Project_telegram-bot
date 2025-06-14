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
import openai
import sys

class Reference:
    '''
    This class will store whatever questions we have asked previously and answer given by chatGPT.
    '''
    def __init__(self) -> None:
        self.response = ""
# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

reference = Reference()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# model name
MODEL_NAME = "gpt-3.5-turbo"

# Initialize not and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher()

def clear_past():
    """
    This function clears the previous conversation and context.
    """
    reference.response = ""

# The following code is from: https://docs.aiogram.dev/en/latest/
@dispatcher.message(Command(commands=["start"]))
async def welcome(message:Message):
    """
    This function/handler receives message with '/start' or '/help' command. The following text present in 'message.reply()' will be printed. 
    """
    await message.reply("Hi\nI am Tele Bot!\nCreated by Khanjan. How can I assist you?")

@dispatcher.message(Command(commands=['clear']))
async def clear(message:Message):
    """
    A function/handler to clear the previous conversation by calling the function 'clear_past()'.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")

@dispatcher.message(Command(commands=['help']))
async def helper(message: Message):
    """
    A function/handler to display the help menu.
    """
    help_command = """
    Hi There, I'm chatGPT Telegram bot created by Khanjan. Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context
    /help - to get this help menu.
    I hope this helps. :) 
    """
    await message.reply(help_command)

@dispatcher.message()
async def chatgpt(message: Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    try:
        response = openai.ChatCompletion.create(
            model = MODEL_NAME,
            messages = [
                {"role":"assistant","content":reference.response}, # role assistant
                {"role":"user","content":message.text} # our query
            ]
        )
        # Both the following lines of code works.
        #reference.response = response.choices[0]['message']['content']
        reference.response = response.choices[0].message['content']
    except Exception as e:
        reference.response = "An error occurred:"+str(e)
    print(f">>> chatGPT:\n\t{reference.response}")
    await bot.send_message(chat_id=message.chat.id, text=reference.response)

async def main():
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

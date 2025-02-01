import logging
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os
import openai
import sys

load_dotenv()
openai.api_key=os.getenv("OpenAI_API_Key")
telegram_bot_token=os.getenv("Telegram_bot_token")

class Reference:
    '''
    A class to store previous response from the chatGPT API
    '''
    def __init__(self):
        self.response=""

ref=Reference()

#model name
MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot=Bot(token=telegram_bot_token)
dispatcher=Dispatcher(bot)



@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` command
    """
    await message.reply("Hi\nI am Tele Bot!\Created by Harshit Goswami. How can i assist you?")


@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm chatGPT Telegram bot created by PWskills! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)

def clear_past():
     """
     A function to clear the previous conversation and context.
    """
     ref.response=""

@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    This will clear the previous conversation with bot
    """
    clear_past()
    await message.reply("previous conversation is cleared")

@dispatcher.message_handler()
async def chatgpt_model(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>>USER: \n\t{message.text}")
    response=openai.ChatCompletion.create(
        model=MODEL_NAME,
        message=[
            {'role':'assistant','content':ref.response} ,# role assistant(giving previous chats to model)
            {'role':'user','content':message.text} ## query of the user
        ]
    )
    ref.response=response.choices[0]['message']['content']
    print(f">>> chatgpt: \n\t{ref.response}")
    await bot.send_message(chat_id=message.chat.id, text=ref.response)   

# import openai
# import asyncio

# @dispatcher.message_handler()
# async def chatgpt_model(message: types.Message):
#     """
#     A handler to process the user's input and generate a response using the ChatGPT API.
#     """
#     print(f">>> USER: \n\t{message.text}")

#     try:
#         response = await asyncio.to_thread(
#             openai.ChatCompletion.create,
#             model=MODEL_NAME,
#             messages=[  # Fix: "messages" instead of "message"
#                 {'role': 'assistant', 'content': ref.response},
#                 {'role': 'user', 'content': message.text}
#             ],
#             timeout=10  # Set a timeout of 10 seconds
#         )

#         ref.response = response['choices'][0]['message']['content']
#         print(f">>> ChatGPT: \n\t{ref.response}")

#         await bot.send_message(chat_id=message.chat.id, text=ref.response)

#     except openai.error.OpenAIError as e:
#         print(f"OpenAI API Error: {e}")
#         await bot.send_message(chat_id=message.chat.id, text="Sorry, there was an error processing your request.")

#     except Exception as e:
#         print(f"Unexpected Error: {e}")
#         await bot.send_message(chat_id=message.chat.id, text="An unexpected error occurred. Please try again.")




# if __name__ == "__main__":
#     executor.start_polling(dispatcher, skip_updates=False)
if __name__ == "__main__":
    print("🚀 Starting bot polling...")
    executor.start_polling(dispatcher, skip_updates=False)
    print("✅ Polling has ended.")





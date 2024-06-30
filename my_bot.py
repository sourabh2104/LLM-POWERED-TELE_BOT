from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
import openai


load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot 
bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)


class Refrence:
    def __init__(self) -> None:
        self.response = ""

reference = Refrence()

def clear_past():
    reference.response = ""


@dispatcher.message_handler(commands = ['start','help'])
async def command_start_handler(message: 
type.Message):
    """This handler receives messages with '/sta
or '/help 'command

    Args:
        messages (types.Message): _description_
    """
    
await message.reply("Hi!\n I am a Chat Bot! Created by Sourabh. How can i assist you?")


@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to dispaly the help menu.
    """
    help_command = """
    Hi There I'm a bot created by Sourabh! please follow these commands -
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get the help menu.
    I hope this helps. :)
    """

await message.reply(help_command)

    
@dispatcher.message_handler(commands = ['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """

    clear_past()
    await message.reply("I've cleared the past conversations and context")


@dispatcher.message_handler()
async def main_bot(message: types.Message):
 """
    A handler to process the user's input and generate a response a using the openai API.'
    """

print(f">>> USER: \n\t{message.text}")
response = openai.ChatCompletion.create(
    model = MODEL_NAME,
    message = [
        {"role": "assistant", "content":reference.response}, #role assistant
        {"role": "user","content":message.text} # our query
        ]
    )
reference.response = response['choices'][0]['message']['content']
print(f">>> chatGPT: \n\t{reference.response}")
await bot.send_message(chat_id = message.chat.id, text = reference.response)

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
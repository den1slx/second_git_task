import os
import telegram


token = os.environ['TG_TOKEN']
bot = telegram.Bot(token=token)
chat_id = '@channerfortest'

bot.send_message(chat_id=chat_id, text='Hello word')

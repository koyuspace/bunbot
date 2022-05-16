#!/usr/bin/python3
import telegram
import time
import os
import json
import urllib.request
import logging
from telegram.error import NetworkError, Unauthorized

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get("TOKEN")
else:
     TOKEN = ""   

def handle(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.effective_message and update.effective_message.text:
            chat_id = update.effective_message.chat_id
            if update.effective_message["text"].startswith("/start"):
                bot.sendMessage(chat_id, "Hello, I'm bunbot. If you enter a command starting with bun or similar I'll post a picture of a bunny.")
            if update.effective_message["text"].startswith("/bun") or update.effective_message["text"].startswith("/bnu"):
                jsondata = json.loads(urllib.request.urlopen("https://api.tinyfox.dev/img?animal=bun&json").read())
                bot.sendPhoto(chat_id, "https://api.tinyfox.dev/"+jsondata["loc"], reply_to_message_id=update.effective_message.message_id)

print('Listening ...')

def main():
    global update_id
    bot = telegram.Bot(TOKEN)
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            handle(bot)
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            update_id += 1

if __name__ == '__main__':
    main()
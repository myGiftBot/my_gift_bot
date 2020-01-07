# -*- coding: utf-8 -*-

import telebot
import os

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get("TOKEN")
else:
    from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
     bot.infinity_polling()
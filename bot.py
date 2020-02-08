# -*- coding: utf-8 -*-

import telebot
import os
import flask
import logging

from telebot import types

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get("TOKEN")
else:
    from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    # bot.reply_to(message,
    #              ("Hi there, I am EchoBot.\n"
    #               "I am here to echo your kind words back to you."))
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Баланс")
    # item2 = types.KeyboardButton("😊 Как дела?")

    markup.add(item1)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\n"
                     "Я - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['balance'])
def send_balance(message):
    from balance import check_balance
    bot.reply_to(message, check_balance())


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == "Баланс":
            from balance import check_balance
            bot.send_message(message.chat.id, check_balance())


if __name__ == '__main__':
    if 'TOKEN' in os.environ:
        logger = telebot.logger
        telebot.logger.setLevel(logging.INFO)

        server = flask.Flask(__name__)


        @server.route('/' + TOKEN, methods=['POST'])
        def getMessage():
            bot.process_new_updates([telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))])
            return "!", 200


        @server.route("/")
        def webhook():
            bot.remove_webhook()
            bot.set_webhook(url=os.environ.get("APP_URL") + TOKEN)
            return "Hello!", 200


        server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
    else:
        telebot.apihelper.proxy = {'https': 'socks5://211299130:Okrv20YQ@orbtl.s5.opennetwork.cc:999'}
        bot.remove_webhook()
        bot.polling(none_stop=True)

# -*- coding: utf-8 -*-

import telebot
import os
import flask
import logging

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get("TOKEN")
else:
    from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi there, I am EchoBot.\n"
                  "I am here to echo your kind words back to you."))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    if 'TOKEN' in os.environ:
        logger = telebot.logger
        telebot.logger.setLevel(logging.INFO)

        server = flask.Flask(__name__)


        @server.route("/bot", methods=['POST'])
        def getMessage():
            bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
            return "!", 200


        @server.route("/")
        def webhook():
            bot.remove_webhook()
            bot.set_webhook(
                url=os.environ.get("APP_URL"))  # этот url нужно заменить на url вашего Хероку приложения
            return "?", 200


        server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
    else:
        telebot.apihelper.proxy = {'https': 'socks5://211299130:Okrv20YQ@orbtl.s5.opennetwork.cc:999'}
        bot.remove_webhook()
        bot.polling(none_stop=True)

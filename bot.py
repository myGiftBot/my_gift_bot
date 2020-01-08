# -*- coding: utf-8 -*-

import telebot
import os
import time
import flask

if 'TOKEN' in os.environ:
    TOKEN = os.environ.get("TOKEN")
    app = flask.Flask(__name__)
    WEBHOOK_HOST = '<ip/host where the bot is running>'
    WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
    WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
    WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
    WEBHOOK_URL_PATH = "/%s/" % TOKEN

else:
    from config import TOKEN

    telebot.apihelper.proxy = {'https': 'socks5://211299130:Okrv20YQ@orbtl.s5.opennetwork.cc:999'}

bot = telebot.TeleBot(TOKEN)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


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
        bot.remove_webhook()
        time.sleep(0.1)
        bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
        app.run(host=WEBHOOK_LISTEN,
                port=WEBHOOK_PORT)
    else:
        bot.infinity_polling()

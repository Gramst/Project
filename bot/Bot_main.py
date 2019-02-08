import datetime
import logging
import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, CallbackQueryHandler

import Bot_settings as sett
from Handlers import greet_user, atm_search, user_settings, proc_location, f_cancel, proc_location, proc_message, f_callback, money_exchange
from Bot_users import Users
from Yandex_api import YandexApi

users = Users(sett.PATH)
yandex = YandexApi(sett.Y_TOKEN, sett.PATH)



logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

PROXY = {'proxy_url': 'socks5h://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}


def main():
    mybot = Updater(sett.TOKEN, request_kwargs=PROXY)
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler("start", greet_user))

    dp.add_handler(RegexHandler('^(Найти банкомат)$', atm_search))
    dp.add_handler(RegexHandler('^(Обмен валюты)$', money_exchange))
    dp.add_handler(RegexHandler('^(Настройки)$', user_settings))
    dp.add_handler(RegexHandler('^(Отмена)$', f_cancel))

    dp.add_handler(CallbackQueryHandler(f_callback)) #'^(need_geo)$',

    dp.add_handler(MessageHandler(Filters.location, proc_location))
    dp.add_handler(MessageHandler(Filters.text, proc_message))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()

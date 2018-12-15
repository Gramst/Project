import datetime
import logging
import random

from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton, InlineKeyboardMarkup

import Bot_settings as sett
import Bot_text as b_text
from Bot_users import Users
from Yandex_api import Yndx_api

users = Users(sett.PATH)
yandex = Yndx_api(sett.Y_TOKEN, sett.PATH)


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

PROXY = {'proxy_url': 'socks5h://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

keyboards = {

    'test': 
    [
    [InlineKeyboardButton("Точка 1", callback_data='1'),
    InlineKeyboardButton("Точка 2", callback_data='2')],
    [InlineKeyboardButton("Использовать геолокацию", callback_data='need_geo')]
    ],

    'global_keyboard' : 
    [
    ["Обмен валюты", "Найти банкомат"],
    ["Поиск вклада", "Настройки"]
    ],

    'need_geo' : 
    [
    [KeyboardButton('Отправить геолокацию', request_location=True)],
    ['Отмена']
    ],
    'atm_search_k' : 
    [
    ["Сбербанк", "ОТП Банк"],
    ["Райфайзен", "Тула Банк"],
    ['Любой ближайший']
    ['Отмена']
    ]    
    'sett_keyboard' : 
    [
    [KeyboardButton('Тест гео', request_location=True)],
    ["Отмена"]
    ],
}


def send(my_bot_f):
    def wrapper_arg(bot, update):
        text, keyboard = my_bot_f(bot, update)
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    return wrapper_arg


@send
def greet_user(bot, update):
    user_id = update['message']['chat']['id']

    if not users.search(user_id):
        users.new_user(user_id)
        text = b_text.greeting_t
    else:
        text = b_text.help_t
        
    keyboard = keyboards['global_keyboard']

    return text, keyboard


@send
def f_cancel(bot, update):

    user_id = update.message.chat.id

    users.reset_state(user_id)
    text = b_text.reset_t + '\n' + b_text.help_t
    keyboard = keyboards['global_keyboard']
    
    return text, keyboard


def money_exchange(bot, update):
    pass


@send
def atm_search(bot, update):
    user_id = update.message.chat.id
    users.set_state(user_id, 'atm')
    text = b_text.atm_search_t
    reyboard = keyboards['need_geo']

    return text, keyboard


def money_search(bot, update):
    pass

@send
def user_settings(bot, update):
    user_id = update.message.chat.id
    users.set_state(user_id, 'sett')
    text = b_text.settings_t
    keyboard = keyboards['sett_keyboard']
    
    return text, keyboard


@send
def f_settings_get_location(bot, update, longitude, latitude):
    text = yandex.get_location(longitude,latitude)
    keyboard = keyboards['sett_keyboard']
    return text, keyboard


@send
def f_atm_get_location(bot, update, longitude, latitude):
    ...


@send
def f_atm_get_bank_name(bot, update):
    user_id = update.message.chat.id

    if update.message.text != 'Любой ближайший'
        users.add_searched_name(user_id, update.message.text)
        text = b_text.atm_search_get_name_t.format(update.message.text)
    else:

    ...


def proc_message(bot, update):

    state = users.get_state(user_id)
    print(state)

    if state == error:
        f_cancel(bot, update)

    elif state = 'atm':
        f_atm_get_bank_name(bot, update)

    else:
        greet_user(bot, update)


def proc_location(bot, update):

    user_id = update.message.chat.id
    longitude = update.message.location['longitude']
    latitude = update.message.location['latitude']

    state = users.get_state(user_id)
    print(state)

    if state == 'sett' :
        f_settings_get_location(bot, update, longitude, latitude)

    elif state == 'atm':
        atm = users.get_searched_name(user_id)
        f_atm_get_location(bot, update, longitude, latitude)

    else:
        f_cancel(bot, update)


def main():
    mybot = Updater(sett.TOKEN, request_kwargs=PROXY)
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler("start", greet_user))

    dp.add_handler(RegexHandler('^(Найти банкомат)$', atm_search))
    dp.add_handler(RegexHandler('^(Настройки)$', user_settings))
    dp.add_handler(RegexHandler('^(Отмена)$', f_cancel))

    # dp.add_handler(CallbackQueryHandler(f_need_geo)) #'^(need_geo)$',

    dp.add_handler(MessageHandler(Filters.location, proc_location))
    dp.add_handler(MessageHandler(Filters.text, proc_message))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
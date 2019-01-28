from telegram import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton, InlineKeyboardMarkup

from Bot_users import Users
from Yandex_api import YandexApi
import Bot_text as b_text
import Bot_settings as sett

users = Users(sett.PATH)
yandex = YandexApi(sett.Y_TOKEN, sett.PATH)

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
    ['Любой ближайший'],
    ['Отмена']
    ],
    'sett_keyboard' : 
    [
    [KeyboardButton('Тест гео', request_location=True)],
    ["Отмена"]
    ],
}

def bild_inline_keyboard(self_coord=None, list_bank_coordinates=None):
    #TODO проверка нанов
    sc = self_coord
    lbc = list_bank_coordinates
    atm_out = []
    n = 1
    for atm in lbc:
        line = [InlineKeyboardButton("ATM {0}".format(n), callback_data='sln={0}slt{1}tln={2}tlt{3}'\
            .format(sc[0],sc[1],atm['geo'][0],atm['geo'][1]))] #,atm['name']))]
        atm_out.append(line[0])
        n+=1
    print(atm_out)
    menu = [] 
    i = 0
    while i<len(atm_out):
        menu.append(atm_out[i:i+3])
        i+=3
    print(menu)
    reply_markup = InlineKeyboardMarkup(menu)
    return reply_markup

def greet_user(bot, update):
    user_id = update['message']['chat']['id']

    if not users.search(user_id):
        users.new_user(user_id)
        text = b_text.greeting_t
    else:
        text = b_text.help_t
        
    keyboard = keyboards['global_keyboard']

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")


def f_cancel(bot, update):

    user_id = update.message.chat.id

    users.reset_state(user_id)
    text = b_text.reset_t + '\n' + b_text.help_t
    keyboard = keyboards['global_keyboard']
    

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def money_exchange(bot, update):
    pass


def atm_search(bot, update):
    user_id = update.message.chat.id
    users.set_state(user_id, 'atm')
    text = b_text.atm_search_t
    keyboard = keyboards['atm_search_k'] 


    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def money_search(bot, update):
    pass

def user_settings(bot, update):
    user_id = update.message.chat.id
    users.set_state(user_id, 'sett')
    text = b_text.settings_t
    keyboard = keyboards['sett_keyboard']

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def f_settings_get_location(bot, update, longitude, latitude):
    text = yandex.get_location(longitude,latitude)
    keyboard = keyboards['sett_keyboard']
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")


def f_atm_get_location(bot, update, longitude, latitude, atm):
    text, ld_of_atms = yandex.search_atm(longitude, latitude, atm)
    #keyboard = keyboards['atm_out']
    reply_markup = bild_inline_keyboard([longitude, latitude], ld_of_atms) 
    update.message.reply_text(text, reply_markup=reply_markup)
    
def f_get_bank_name(bot, update):
    user_id = update.message.chat.id
   
    state_user = users.get_state(user_id)

    if state_user == 'atm':
        searched_name == 'банкомат'
    elif state_user == 'error' or state_user == None:
        f_cancel()

    if update.message.text != 'Любой ближайший':
        print(update.message.text)
        users.add_searched_name(user_id, update.message.text)
        text = b_text.atm_search_get_name_t.format(update.message.text)
    else:
        users.add_searched_name(user_id, 'Банкомат')
        text = b_text.atm_search_get_name_t.format(update.message.text)

    keyboard = keyboards['need_geo']
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")


def f_atm_get_bank_name(bot, update):
    user_id = update.message.chat.id

    if update.message.text != 'Любой ближайший':
        print(update.message.text)
        users.add_searched_name(user_id, update.message.text)
    else:
        users.add_searched_name(user_id, 'Банкомат')

    text = b_text.atm_search_get_name_t.format(update.message.text)

    keyboard = keyboards['need_geo']
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")


def proc_message(bot, update):

    user_id = update.message.chat.id
    state = users.get_state(user_id)
    print(state)

    if state == 'error':
        f_cancel(bot, update)

    elif state == 'atm':
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
        f_atm_get_location(bot, update, longitude, latitude, atm)

    else:
        f_cancel(bot, update)



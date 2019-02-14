import re
import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton, InlineKeyboardMarkup

from users_bot import Users
from api_yandex import YandexApi
import Bot_text as b_text
import Bot_settings as sett
import cvs_read as csvr

users = Users(sett.PATH)
yandex = YandexApi(sett.Y_TOKEN, sett.PATH)
cities_d = csvr.get_dict()
mod_log = logging.getLogger('Handlers')

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
    [ "Настройки"]
    ],

    'money_search_k' :
    [
    ["Волгоград", "Брест"],
    ['Отмена']
    ],

    'need_geo' : 
    [
    [KeyboardButton('Отправить геолокацию', request_location=True)],
    ['Отмена']
    ],

    'atm_search_k' : 
    [
    ["Сбербанк", "БПС Сбербанк"],
    ["Райфайзен", "Приорбанк"],
    ['Любой ближайший'],
    ['Отмена']
    ],

    'sett_keyboard' : 
    [
    [KeyboardButton('Тест гео', request_location=True)],
    ["Отмена"]
    ],
}
def bild_keyboard_low(buttons=None, row=2):
#buttons = { 'name': ... 'call' : .... }
    atm_out = buttons
    mod_log.info(atm_out)
    menu = [] 
    i = 0
    while i<len(atm_out):
        menu.append(atm_out[i:i+row])
        i+=row
    menu.append(['Отмена'])
    mod_log.info(menu)
    return menu



def bild_keyboard(buttons=None, row=2):
#buttons = { 'name': ... 'call' : .... }
    atm_out = []
    lbc = buttons
    n = 1
    for i in lbc:
        line = [InlineKeyboardButton("{0}".format(lbc[i]['name']), callback_data='{0}'\
            .format( lbc[i]['call']))]
        atm_out.append(line[0])
        n+=1
    mod_log.info(atm_out)
    menu = [] 
    i = 0
    while i<len(atm_out):
        menu.append(atm_out[i:i+row])
        i+=row
    mod_log.info(menu)
    reply_markup = InlineKeyboardMarkup(menu)
    return reply_markup

def bild_atm_keyboard(self_coord=None, list_bank_coordinates=None, mode=0):
    #TODO проверка нанов
    sc = self_coord
    lbc = list_bank_coordinates
    atm_out = []
    n = 1
    for atm in lbc:
        line = [InlineKeyboardButton("Место {0}".format(n), callback_data='mode={4}sln={0}slt{1}tln={2}tlt{3}'\
            .format(sc[0], sc[1], atm['geo'][0], atm['geo'][1], mode))] #,atm['name']))]
        atm_out.append(line[0])
        n+=1
    mod_log.info(atm_out)
    menu = [] 
    i = 0
    while i<len(atm_out):
        menu.append(atm_out[i:i+3])
        i+=3
    mod_log.info(menu)
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


def f_cancel(bot, update, text=b_text.reset_t + '\n' + b_text.help_t):
    mod_log.info('f_cancel')

    user_id = update.message.chat.id

    users.reset_state(user_id)

    keyboard = keyboards['global_keyboard']
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def money_exchange(bot, update):
    user_id = update.message.chat.id
    users.set_state(user_id, 'money')
    text = b_text.money
    city = {}
    city[1] = {}
    city[1]['name'] = 'Волгоград'
    city[1]['call'] = 'mode=2city=VLG'
    city[2] = {}
    city[2]['name'] = 'Брест'
    city[2]['call'] = 'mode=2city=BST'
    reply_markup = bild_keyboard(city, 1) 
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")



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
    reply_markup = bild_atm_keyboard([longitude, latitude], ld_of_atms) 
    update.message.reply_text(text, reply_markup=reply_markup)
    
def f_atm_get_bank_name(bot, update):
    user_id = update.message.chat.id

    if update.message.text != 'Любой ближайший':
        mod_log.info(update.message.text)
        users.add_searched_name(user_id, update.message.text)
    else:
        users.add_searched_name(user_id, ' ')

    text = b_text.atm_search_get_name_t.format(update.message.text)

    keyboard = keyboards['need_geo']
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def f_money_get_bank_name(bot, update):
    user_id = update.message.chat.id

    if update.message.text != 'Любой ближайший':
        mod_log.info(update.message.text)
        users.add_searched_name(user_id, update.message.text)
    else:
        users.add_searched_name(user_id, ' ')

    text = b_text.money_search_get_name_t.format(update.message.text)

    keyboard = keyboards['need_geo']
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

def proc_message(bot, update):

    user_id = update.message.chat.id
    state = users.get_state(user_id)
    mod_log.info(state)

    if state == 'error' or update.message.text == 'Отмена':
        f_cancel(bot, update)

    elif state == 'atm':
        f_atm_get_bank_name(bot, update)

    elif state == 'money':
        f_money_get_bank_name(bot, update)

    else:
        greet_user(bot, update)


def proc_location(bot, update):

    user_id = update.message.chat.id
    longitude = update.message.location['longitude']
    latitude = update.message.location['latitude']

    state = users.get_state(user_id)
    mod_log.info(state)

    if state == 'sett' :
        f_settings_get_location(bot, update, longitude, latitude)

    elif state == 'atm':
        atm = users.get_searched_name(user_id) + ' банкомат'
        mod_log.info(atm)
        f_atm_get_location(bot, update, longitude, latitude, atm)

    elif state == 'money':
        money =users.get_searched_name(user_id) + ' обменник'
        mod_log.info(money)
        f_atm_get_location(bot, update, longitude, latitude, money)

    else:
        f_cancel(bot, update)

def f_callback(bot, update):
#"""
#mode:
#0-получить карту
#5-изменить список банков
#"""
    mod_log.info('f_callback')
    user_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id

    rs = re.findall(r'mode=(.)', update.callback_query.data)
    if rs[0][0] == '0':
        _f_get_map(bot, user_id, update.callback_query.data)
    if rs[0][0] == '5':
        _f_users_set_new_bank_list(bot, user_id, update.callback_query.data)
    if rs[0][0] == '2':
        _f_select_valut(bot, user_id, update.callback_query.data, message_id)
    if rs[0][0] == '3':
        _f_get_bank_list_button(bot, user_id, update.callback_query.data, message_id)
    if rs[0][0] == '4':
        _f_get_bank_list(bot, user_id, update.callback_query.data, message_id, update)

def _f_get_map(bot, user_id, income_callback_data):
    mod_log.info('_f_get_map')
    rs = re.findall(r'mode=(.)sln=(.*)slt(.*)tln=(.*)tlt(.*)', income_callback_data)
    text = '[***Ссылка на карту***](' + yandex.get_url_static_map(rs[0][1], rs[0][2], rs[0][3], rs[0][4]) + ')'
    keyboard = keyboards['global_keyboard']
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    bot.send_message(chat_id=user_id, text=text, parse_mode='Markdown')

def _f_select_valut(bot, user_id, income_callback_data, message_id):
    mod_log.info('_f_get_map')
    rs = re.findall(r'mode=(.)city=(...)', income_callback_data)
    mod_log.info(rs[0][1])
    money = {}
    money[1] = {}
    money[1]['name'] = 'RUB->USD'
    money[1]['call'] = 'mode=3city={0}val=rur_usd'.format(rs[0][1])
    money[2] = {}
    money[2]['name'] = 'RUB->EUR'
    money[2]['call'] = 'mode=3city={0}val=rur_eur'.format(rs[0][1])
    money[3] = {}
    money[3]['name'] = 'USD->RUB'
    money[3]['call'] = 'mode=3city={0}val=usd_rur'.format(rs[0][1])
    money[4] = {}
    money[4]['name'] = 'EUR->RUB'
    money[4]['call'] = 'mode=3city={0}val=eur_rur'.format(rs[0][1])
    reply_markup = bild_keyboard(money, 2) 
    #update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=reply_markup)


def _f_get_bank_list_button(bot, user_id, income_callback_data, message_id):
    rs = re.findall(r'mode=(.)city=(.{3})val=(.{7})', income_callback_data)
    money = {}
    money[1] = {}
    money[1]['name'] = 'Искать гор. {0} пара:{1}'.format(rs[0][1], rs[0][2])
    money[1]['call'] = 'mode=4city={0}val=rur_usd'.format(rs[0][1])
    reply_markup = bild_keyboard(money, 1) 
    
    bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=reply_markup)

def _f_get_bank_list(bot, user_id, income_callback_data, message_id, update):
    rs = re.findall(r'mode=(.)city=(.{3})val=(.{7})', income_callback_data)
    state = users.get_state(user_id)
    mod_log.info(state)
    dict_to_send = csvr.get_kurs(cities_d, rs[0][1], rs[0][2])
    mod_log.info(dict_to_send)
    menu = []
    text = 'Выберите обменник:\n\n'
    for i in dict_to_send:
        text +=' {0:<20} курс **{1}**\n\n'.format(i, dict_to_send[i])
        menu.append(i)
    keyboard = bild_keyboard_low(menu)

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    bot.send_message(chat_id=user_id, text=text,  reply_markup=reply_markup, parse_mode='Markdown')


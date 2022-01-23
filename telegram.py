# !/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the private license.

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
import requests
# import socket
# import socks
import random
import logging
# import json

from flask import Flask, request

import telebot

from telebot import types
from telebot.types import Message
from telebot import apihelper

# MAIN_URL = f'https://api.telegram.org/bot{TOKEN}'
TIBO_TELEGRAM_BOT_TOKEN = os.environ['TIBO_TELEGRAM_BOT_TOKEN']
# TOKEN = '1007635405:AAGne0oJ0ERYnAftVfCUwFc3ZIaDzf-NDSU'
OPEN_WAETHER_MAP_TOKEN = 'e92f4ab649c62931261157c7cf958e1d'
# TIMEZONE = 'Asia/Yekaterinburg'
# TIMEZONE_COMMON_NAME = 'Yekaterinburg'
# P_TIMEZONE = pytz.timezone(config.TIMEZONE)
# TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME

proxy_bank = {
    "proxy_list": {
        "ip": "96.96.33.133",
        "port": 1080,
        "username": "",
        "password": "",
        "from": "http://free-proxy.cz/ru/proxylist/country/all/socks5/speed/all"
    },
    "proxy_list2": {
        "ip": "149.28.79.225",
        "port": 3128,
        "username": "",
        "password": "",
        "from": "https://hidemy.name/ru/proxy-list/"
    },
    "proxy_bot": {
        "ip": "grsst.s5.opennetwork.cc",
        "port": 999,
        "username": "41365750",
        "password": "QSztxzyl",
        "from": "@socks5_bot"
    },
    "proxy_bot2": {
        "ip": "148.251.234.93",
        "port": 1080,
        "username": "41365750",
        "password": "QSztxzyl",
        "from": "https://sockslist.net/"
    }
}

current_proxy = proxy_bank["proxy_list2"]
proxy = f'socks5h://{current_proxy["ip"]}:{current_proxy["port"]}'


# proxy = f'socks5h://{current_proxy["username"]}:{current_proxy["password"]}@{current_proxy["ip"]}:{current_proxy["port"]}'

# socks.set_default_proxy(socks.SOCKS5, current_proxy["ip"], current_proxy["port"])
# socket.socket = socks.socksocket


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TIBO_TELEGRAM_BOT_TOKEN)
bot.set_update_listener(listener)  # register listener
STICKERID = 'CAACAgIAAxkBAAMbXrPw-PFI1fxdd1PM4gvH4ByBzU8AAqwAA1dPFQieKyFie6ajbxkE'

# USERS = set()

telebot.logger.setLevel(logging.DEBUG)

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start': 'Get used to the bot',
    'help': 'Gives you information about the available commands',
    'getimage': 'A test using multi-stage messages, custom keyboard, and media sending',
    'weather': 'OpenWeatherMap data',
    'погода': 'по-русски',
    'bar': 'GO DRINK',
    'mem': 'send memories'
}

beer_photo = [
    "https://img1.thelist.com/img/gallery/what-happens-to-your-body-when-you-drink-beer-every-night/intro-1577191347.jpg",
    "https://i.ytimg.com/vi/TumxeIPQfTI/maxresdefault.jpg",
    "https://media-cdn.tripadvisor.com/media/photo-s/10/bd/94/25/drink-beer.jpg",
    "https://media.daysoftheyear.com/20171223124045/drink-beer-day1.jpg",
    "https://kajabi-storefronts-production.global.ssl.fastly.net/kajabi-storefronts-production/blogs/15486/images/0snKererQUCYqgNGYGNA_vegan-beer.jpg",
    "https://cdn.craftbeer.com/wp-content/uploads/Craft-Beer-Glasses-1200.jpg",
    "https://static.toiimg.com/thumb/msid-10815880,width-800,height-600,resizemode-75/10815880.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMn1izpSbHb0ClIycPeiePnl1Ct9fG6qmJcBLKSTulaSmaVGyyjg&s",
    "https://www.tasteofhome.com/wp-content/uploads/2019/03/shutterstock_1212903172-line-of-beers.jpg",
    "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/close-up-of-hands-holding-beer-glasses-royalty-free-image-736280003-1534346317.jpg?crop=0.669xw:1.00xh;0.166xw,0&resize=640:*",
    "https://d.newsweek.com/en/full/889150/00.jpg?w=737&f=f9b6f7a8e63a146820640f5531752c0c",
    "https://media.npr.org/assets/img/2018/10/16/rts1u2te-71fe69214f2094429ea5ca2485cd1fbd5ee8383f-s800-c85.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqe0xsBCQK1sR0JyRVofx3oJns30ApYA1pk59DpTpdeqxD4Lc1&s",
    "https://www.dw.com/image/43830445_303.jpg",
    "https://www.ft.com/__origami/service/image/v2/images/raw/http://prod-upp-image-read.ft.com/8db8265e-1cff-11ea-81f0-0c253907d3e0?source=next&fit=scale-down&quality=highest&width=1067",
    "https://static-38.sinclairstoryline.com/resources/media/95577ddb-38e7-4480-9723-81b89498a10f-large1x1_MGN_1280x960_70804P00KLNAV.jpg?1587064678520",
    "https://upload.wikimedia.org/wikipedia/commons/d/db/Aufse%C3%9F_Bier.JPG",
    "https://img.washingtonpost.com/rf/image_1484w/2010-2019/WashingtonPost/2017/02/01/Food/Images/food_011-004.JPG?uuid=_NMimOgwEeaQPZsR7X2NKg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQo85_Z348eJyMvHDtwy-BcLl8B1XltoHaK1xhcUr7sEcQDWGZT&s",
    "https://katu.com/resources/media/bad96236-45dd-405d-895a-89a85b619707-large16x9_manifest4.PNG?1588253194556",
    "https://www.mlive.com/resizer/OhjAoigJKQKOsIbXWO6Gwd-Week=/450x0/smart/image.mlive.com/home/mlive-media/width600/img/michigan_beer/photo/2017/09/28/celebrate-national-drink-beer-day-01020f2d1f374e07.jpg"
]

bar_members = {
    '41365750': {
        'username': 'csredrat',
        'first': 'Sergey'
    },
    '670403191': {
        'username': 'elijah_here',
        'first': 'Илья',
        'last': 'Полосков'
    },
    '1006923818': {
        'first': 'James',
        'last': 'Touchet'
    },
    '61049840': {
        'first': 'Pavel',
        'last': 'S'
    },
    '652907968': {
        'first': 'Nikita'
    }
}


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        bot.send_message(cid, "Hello, stranger, let me scan you...")
        bot.send_message(cid, "Scanning complete, I know you now")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "I already know you, no need for me to scan you again!")


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + " - "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


default_city = 'Perm'


def weather_get(apikey, city):
    try:
        r = requests.get("https://api.openweathermap.org/data/2.5/weather",
                         params={'q': city, 'units': 'metric', 'APPID': apikey})
    except Exception as e:
        print("Exception (forecast):", e)
    return (r.json())


@bot.message_handler(commands=['weather', 'погода'])
def command_weather(message: Message):
    cid = message.chat.id
    command_params = message.text.split()
    params_count = len(command_params)
    city = command_params[1] if params_count > 1 else default_city
    weather = weather_get(OPEN_WAETHER_MAP_TOKEN, city)
    print(weather)
    conditions = weather['weather'][0]['description']
    current_temp = weather['main']['temp']
    temp_min = weather['main']['temp_min']
    temp_max = weather['main']['temp_max']
    bot.send_message(cid,
                     f'{current_temp} {conditions}, up to {temp_max}, at night {temp_min}')


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))


@bot.message_handler(commands=['bar'])
def command_weather(message: Message):
    cid = message.chat.id
    chat = bot.get_chat(message.chat.id)
    mention = []
    for i in bar_members:
        if 'username' in bar_members[i]:
            user = bar_members[i].get('username')
            mention.append(f'@{user}')
        else:
            first = bar_members[i].get('first')
            last = bar_members[i].get('last')
            mention.append(f'<a href="tg://user?id={i}">{first} {last}</a>')
    random.shuffle(mention)
    print(mention)
    push_alert = listToString(mention)
    print(push_alert)
    bot.send_message(cid, f'{push_alert} GO BAR', parse_mode="HTML")
    bot.send_poll(cid, 'DRINK BEER SAVE WATER', ["Drink beer", "Discord", "Play computer"], is_anonymous=False)
    pic_choise = random.randint(0, len(beer_photo))
    bot.send_photo(cid, beer_photo[pic_choise])
    # bot.send_poll(cid, 'Poll', {
    #     "Drink beer",
    #     "Play computer"
    # })


@bot.message_handler(commands=['mem'])
def command_weather(message: Message):
    cid = message.chat.id
    r = requests.get("https://api.imgflip.com/get_memes")
    print(r.content)
    json_data = r.json()
    list_mem = json_data['data']['memes']
    # print(list_mem)
    count_memes = len(list_mem)
    mem = []
    for i in range(0, count_memes):
        mem.append(json_data['data']['memes'][i]['url'])
        # print(mem[i])
    random.shuffle(mem)
    bot.send_photo(cid, mem[0])


@bot.message_handler(commands=['help_auth'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Message the developer', url='telegram.me/csredrat'
        )
    )
    bot.send_message(
        message.chat.id,
        'The bot supports inline. Type @<botusername> in any chat',
        reply_markup=keyboard
    )


# @bot.message_handler(content_types=['text'])
# @bot.edited_message_handler(content_types=['text'])
# def echo_digits(message: Message):
#     print(message.from_user)
#     print(message.from_user.username)
#     if 'Alex Goodkid' in message.text:
#         bot.reply_to(message, 'Alex is good kid')
#         return
#     reply = str(random.random())
#     if message.from_user.id in USERS:
#         reply += f"  {message.from_user.username}, hello again"
#     bot.reply_to(message, reply)
#     USERS.add(message.from_user.id)


@bot.message_handler(content_types=['sticker'])
def sticker_handler(message: Message):
    bot.send_sticker(message.chat.id, STICKERID)
    # print(message)
    # print(message.sticker)


# @bot.inline_handler(lambda query: query.query == 'text')
# def query_text(inline_query):
#     try:
#         print(inline_query)
#         bot.send_chat_action(message, 'typing')
#         r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
#         r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
#         bot.answer_inline_query(inline_query.id, [r, r2])
#     except Exception as e:
#         print(e)


@bot.inline_handler(lambda query: len(query.query.split()) == 0)
@bot.inline_handler(lambda query: len(query.query.split()) == 1)
@bot.inline_handler(lambda query: len(query.query.split()) == 2)
@bot.inline_handler(lambda query: len(query.query.split()) == 3)
@bot.inline_handler(lambda query: len(query.query.split()) == 4)
@bot.inline_handler(lambda query: len(query.query.split()) == 5)
@bot.inline_handler(lambda query: len(query.query.split()) == 6)
@bot.inline_handler(lambda query: len(query.query.split()) == 7)
@bot.inline_handler(lambda query: len(query.query.split()) == 8)
@bot.inline_handler(lambda query: len(query.query.split()) == 9)
@bot.inline_handler(lambda query: len(query.query.split()) == 10)
@bot.inline_handler(lambda query: len(query.query.split()) == 11)
@bot.inline_handler(lambda query: len(query.query.split()) == 12)
@bot.inline_handler(lambda query: len(query.query.split()) == 13)
@bot.inline_handler(lambda query: len(query.query.split()) == 14)
@bot.inline_handler(lambda query: len(query.query.split()) == 15)
@bot.inline_handler(lambda query: len(query.query.split()) == 16)
@bot.inline_handler(lambda query: len(query.query.split()) == 18)
@bot.inline_handler(lambda query: len(query.query.split()) == 19)
@bot.inline_handler(lambda query: len(query.query.split()) == 20)
def query_text(inline_query):
    try:
        text = inline_query.query
        print(inline_query)
        thumbb = 'https://codebridgeplus.com/wp-content/uploads/bold.jpg'
        thumbc = 'https://cdn0.iconfinder.com/data/icons/communication-technology/500/code_brackets-512.png'
        thumbi = 'https://banner2.cleanpng.com/20180409/wiq/kisspng-computer-icons-html-element-ping-pong-5acc02f43d00e8.2242970015233195402499.jpg'
        git_rp = 'https://github.githubassets.com/images/modules/logos_page/Octocat.png'
        googlepic = 'http://cdn.geekwire.com/wp-content/uploads/2015/09/Screen-Shot-2015-09-01-at-9.03.40-AM.png'
        code = types.InlineQueryResultArticle('2', 'Code', types.InputTextMessageContent('<code>{}</code>'.format(text),
                                                                                         parse_mode="HTML"),
                                              description='{}'.format(text), thumb_url=thumbc, thumb_width=20,
                                              thumb_height=20)
        bold = types.InlineQueryResultArticle('1', 'Bold',
                                              types.InputTextMessageContent('<b>{}</b>'.format(text),
                                                                            parse_mode="HTML"),
                                              description='{}'.format(text), thumb_url=thumbb, thumb_width=20,
                                              thumb_height=20)
        italic = types.InlineQueryResultArticle('3', 'Italic',
                                                types.InputTextMessageContent('<i>{}</i>'.format(text),
                                                                              parse_mode="HTML"),
                                                description='{}'.format(text), thumb_url=thumbi, thumb_width=20,
                                                thumb_height=20)
        google = types.InlineQueryResultArticle('7', 'Google Search', types.InputTextMessageContent(
            '[{}](https://www.google.com/search?q={})'.format(text, text), parse_mode='Markdown'),
                                                description='Search : {}'.format(text), thumb_url=googlepic)
        githubrepo = types.InlineQueryResultArticle('5', 'Github Search repository', types.InputTextMessageContent(
            '[Found repository](https://github.com/search?=&q={})'.format(text), parse_mode="Markdown"),
                                                    thumb_url=git_rp)
        bot.answer_inline_query(inline_query.id, [code, bold, italic, google, githubrepo], cache_time=1)
    except Exception as e:
        print(e)


# @bot.inline_handler(lambda query: query.query == 'text')
# def query_text(inline_query):
#     try:
#         r = types.InlineQueryResultArticle('1', 'Result1', types.InputTextMessageContent('hi'))
#         r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('hi'))
#         bot.answer_inline_query(inline_query.id, [r, r2])
#     except Exception as e:
#         print(e)
#
#
# @bot.inline_handler(lambda query: query.query == 'photo1')
# def query_photo(inline_query):
#     try:
#         r = types.InlineQueryResultPhoto('1',
#                                          'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/kitten.jpg',
#                                          'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/kitten.jpg',
#                                          input_message_content=types.InputTextMessageContent('hi'))
#         r2 = types.InlineQueryResultPhoto('2',
#                                           'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg',
#                                           'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg')
#         bot.answer_inline_query(inline_query.id, [r, r2], cache_time=1)
#     except Exception as e:
#         print(e)
#
#
# @bot.inline_handler(lambda query: query.query == 'video')
# def query_video(inline_query):
#     try:
#         r = types.InlineQueryResultVideo('1',
#                                          'https://github.com/eternnoir/pyTelegramBotAPI/blob/master/tests/test_data/test_video.mp4?raw=true',
#                                          'video/mp4', 'Video',
#                                          'https://raw.githubusercontent.com/eternnoir/pyTelegramBotAPI/master/examples/detailed_example/rooster.jpg',
#                                          'Title'
#                                          )
#         bot.answer_inline_query(inline_query.id, [r])
#     except Exception as e:
#         print(e)
#
#
# @bot.inline_handler(lambda query: len(query.query) == 0)
# def default_query(inline_query):
#     try:
#         r = types.InlineQueryResultArticle('1', 'default', types.InputTextMessageContent('default'))
#         bot.answer_inline_query(inline_query.id, [r])
#     except Exception as e:
#         print(e)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message: Message):
#     bot.reply_to(message, message.text)
#     bot.send_chat_action(message, 'typing')

app = Flask(__name__)


@app.route('/' + TIBO_TELEGRAM_BOT_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://itmem-bot.herokuapp.com/' + TIBO_TELEGRAM_BOT_TOKEN)
    return "?", 200


if __name__ == "__main__":
    if 'HEROKU' in os.environ:
        # logger = telebot.logger
        # telebot.logger.setLevel(logging.INFO)
        app.run(host="0.0.0.0", port=os.environ.get('PORT', 8443))
        bot.send_message(41365750, 'Bot started in Heroku cloud')
    else:
        apihelper.proxy = {'https': f'{proxy}'}
        bot.send_message(41365750, 'Bot started from IDE over proxy')
        bot.remove_webhook()
        bot.polling(none_stop=True)

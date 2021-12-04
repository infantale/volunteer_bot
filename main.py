import datetime
import re
import subprocess
import uuid

import telebot
from telebot import types

from time import sleep

from config import sdir
from config import token
from db import add_to_db_tasklist, read_data_in_task, init_db, change_tz, get_user_tz
from pars import import_dt, import_text


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])  # Функция отвечает на команды 'start', 'help'
def start_message(message):
    tz_string = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
    bot.send_message(message.chat.id,
                     f"\n"
                     f"\n"
                     f"\n"
                     f"\n"
                     f"")


@bot.message_handler(commands=['timezone'])  # Функция отвечает на комнаду timezone
def answer_message(message):
    try:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Изменить часовой пояс', callback_data='list_timezone'))
        if get_user_tz(message.chat.id) == 'none':
            bot.send_message(message.chat.id, 'Часовой пояс не установлен', reply_markup=keyboard)
        else:
            timezone = get_user_tz(message.chat.id)
            bot.send_message(message.chat.id, timezone, reply_markup=keyboard)
    except:
        sleep(1)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Изменить часовой пояс', callback_data='list_timezone'))
        if get_user_tz(message.chat.id) == 'none':
            bot.send_message(message.chat.id, 'Часовой пояс не установлен', reply_markup=keyboard)
        else:
            timezone = get_user_tz(message.chat.id)
            bot.send_message(message.chat.id, timezone, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])  # Функция обрабатывает текстовые сообщения
def in_text(message):
    try:
        dt, dt_text = import_dt(message.text, get_user_tz(message.chat.id))
        text = import_text(message.text)
        if dt == 'null':
            bot.send_message(message.chat.id, 'Нужно указать время!')
        elif dt == 'old':
            bot.send_message(message.chat.id, 'Это уже в прошлом!')
        elif text == 'null':
            bot.send_message(message.chat.id, 'Нужно указать о чем вам напомнить!')
        else:
            add_task(message.chat.id, text, dt, dt_text)
            answer = 'Я напомню тебе ' + text + ' ' + dt_text
            bot.send_message(message.chat.id, answer)
    except:
        sleep(1)
        print(message.chat.id)
        timezone = get_user_tz(message.chat.id)
        if timezone == 'none':
            bot.send_message(message.chat.id, "Не установлен часовой пояс.\n"
                                              "Для изменения часового пояса введите команду /timezone")
        else:
            dt, dt_text = import_dt(message.text, get_user_tz(message.chat.id))
            text = import_text(message.text)
            if dt == 'null':
                bot.send_message(message.chat.id, 'Нужно указать время!')
            elif dt == 'old':
                bot.send_message(message.chat.id, 'Это уже в прошлом!')
            elif text == 'null':
                bot.send_message(message.chat.id, 'Нужно указать о чем вам напомнить!')
            else:
                add_task(message.chat.id, text, dt, dt_text)
                answer = 'Я напомню тебе ' + text + ' ' + dt_text
                bot.send_message(message.chat.id, answer)


@bot.callback_query_handler(func=lambda call: True)  # Реакция на кнопки
def callback(call):
    if call.data == 'list_timezone':
        list_timezone(call.message.chat.id)
    if call.data.startswith('set_timezone:'):
        timezone = call.data.split(':')[1]
        change_tz(call.message.chat.id, timezone)
        bot.answer_callback_query(call.id, show_alert=True, text='Часовой пояс установлен')
    if call.data == ' через 15 минут':
        later(call)
    if call.data == ' через час':
        later(call)
    if call.data == ' завтра':
        later(call)


if __name__ == '__main__':  # Ожидать входящие сообщения
    init_db()
    bot.polling()

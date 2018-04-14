#!/usr/bin/python
import os
from os import getenv

from telegram import Bot, TelegramError, InlineKeyboardMarkup, InlineKeyboardButton as Btn
from googleapiclient.errors import HttpError
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from youtube import YoutubeClient
from ordered_set import OrderedSet
from contextlib import suppress
from time import sleep
from random import randint
import requests
import json


def upload(video_id, num):
    print('download preview...', end='')
    file_path = f'{video_id}_maxres{num}.jpg'
    with open(file_path, 'wb') as f:
        f.write(requests.get(f'https://i.ytimg.com/vi/{video_id}/maxres{num}.jpg').content)
        print('ok')

    print('upload to youtube...', end='')
    youtube.upload_thumbnail(video_id, file_path)
    os.remove(file_path)
    print('ok')


def thumbnail_button(bot, cfg):
    req = cfg.callback_query
    video_id, num = req.data.split('||')

    if str(req.message.chat.id) != getenv('CHAT'):
        return

    upload(video_id, num)

    f = lambda s, i: " 🆗 " if str(i) == num else s

    return not bot.editMessageReplyMarkup(
        chat_id=req.message.chat.id,
        message_id=req.message.message_id,
        reply_markup=InlineKeyboardMarkup([[
            Btn(f(" 1️⃣  ", 1), callback_data=f"{video_id}||1"),
            Btn(f(" 2️⃣  ", 2), callback_data=f"{video_id}||2"),
            Btn(f(" 3️⃣  ", 3), callback_data=f"{video_id}||3"),
        ]]))


scope = ['https://www.googleapis.com/auth/youtube']
youtube = YoutubeClient(scope)

bot = Updater(getenv('TM_TOKEN'))
bot.dispatcher.add_handler(CallbackQueryHandler(thumbnail_button))
bot.dispatcher.add_error_handler(print)
bot.start_polling()
bot.idle()

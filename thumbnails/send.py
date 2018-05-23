#!/usr/bin/env python3

from __init__ import *
from telegram import Bot, TelegramError, InlineKeyboardMarkup, InlineKeyboardButton as Btn
from googleapiclient.errors import HttpError
from youtube import YoutubeClient
from ordered_set import OrderedSet
from contextlib import suppress
from time import sleep
from random import randint
import config


def load_data_from_file(path):
    path = join(dirname(__file__), path)
    with suppress(FileNotFoundError), open(path) as file:
        return json.load(file) or []
    return []


def save_as_json_to_file(data, path):
    path = join(dirname(__file__), path)
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)


def send():
    try:
        scope = ['https://www.googleapis.com/auth/youtube']
        fromInet = YoutubeClient(scope).fetch_thumbnails_of_new_videos()
        fromFile = load_data_from_file('thumbnails.json')

        queue = OrderedSet(fromInet) - OrderedSet(fromFile)
        ready = OrderedSet()

        env = config.load('config.prod.yml')
        bot = Bot(env['TM_TOKEN'])
        channel = env['DEV_CHAT']

        for video_id in queue:
            try:
                markup = InlineKeyboardMarkup([[
                    Btn(" 1️⃣  ", callback_data=f"{video_id}||1"),
                    Btn(" 2️⃣  ", callback_data=f"{video_id}||2"),
                    Btn(" 3️⃣  ", callback_data=f"{video_id}||3"),
                ]])

                success = True
                for i in range(1, 4):
                    photo_url = f'https://i.ytimg.com/vi_webp/{video_id}/maxres{i}.webp'
                    err = not bot.sendSticker(channel, photo_url, timeout=20,
                                              disable_notification=True,
                                              reply_markup=markup if i == 3 else None)
                    print(f'image {i}: ' + ('err' if err else 'ok'))
                    success &= not err
                    sleep(2)

                if success: ready.append(video_id)
                print(f'{video_id}: {"ok" if success else "err"}')
                sleep(randint(2, 5))
            except TelegramError as e:
                bot.sendMessage(channel, e.message + "\n" + photo_url)

        lost = len(queue) - len(ready)
        save_as_json_to_file(fromFile + list(ready), 'thumbnails.json')
        if lost: return f'Can\'t send {lost} of {len(queue)} videos'
        if not queue: return 'No new videos'
        return 'ok'

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))


if __name__ == '__main__':
    print(send())

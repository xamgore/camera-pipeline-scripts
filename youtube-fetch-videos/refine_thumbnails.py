#!/usr/bin/python
from os import getenv

from telegram import Bot, TelegramError, InlineKeyboardMarkup, InlineKeyboardButton as Btn
from googleapiclient.errors import HttpError
from youtube import YoutubeClient
from ordered_set import OrderedSet
from contextlib import suppress
from time import sleep
from random import randint
import json


def load_data_from_file(path):
    with suppress(FileNotFoundError), open(path) as file:
        return json.load(file) or []
    return []


def save_as_json_to_file(data, path):
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)


if __name__ == '__main__':
    try:
        scope = ['https://www.googleapis.com/auth/youtube']
        fromInet = YoutubeClient(scope).fetch_thumbnails_of_new_videos()
        fromFile = load_data_from_file('thumbnails.json')

        queue = OrderedSet(fromInet) - OrderedSet(fromFile)
        ready = OrderedSet()

        bot = Bot(getenv('TM_TOKEN'))
        channel = getenv('CHAT')

        for video_id in queue:
            with suppress(TelegramError):
                markup = InlineKeyboardMarkup([[
                    Btn(" 1️⃣  ", callback_data=f"{video_id}||1"),
                    Btn(" 2️⃣  ", callback_data=f"{video_id}||2"),
                    Btn(" 3️⃣  ", callback_data=f"{video_id}||3"),
                ]])

                success = True
                for i in range(1, 4):
                    photo_url = f'https://i.ytimg.com/vi_webp/{video_id}/maxres{i}.webp'
                    err = not bot.sendSticker(channel, photo_url, disable_notification=True,
                                             reply_markup=markup if i == 3 else None)
                    print(f'image {i}: ' + ('err' if err else 'ok'))
                    success &= not err
                    sleep(2)

                if success: ready.append(video_id)
                print(f'{video_id}: {"ok" if success else "err"}')
                sleep(randint(2, 5))

        lost = len(queue) - len(ready)
        if lost: print(f'Can\'t send {lost} of {len(queue)} videos')
        if not queue: print('No new videos')

        save_as_json_to_file(fromFile + list(ready), 'thumbnails.json')

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

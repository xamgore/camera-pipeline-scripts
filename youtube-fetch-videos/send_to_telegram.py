#!/usr/bin/python
from os import getenv

from telegram import Bot, TelegramError
from googleapiclient.errors import HttpError
from youtube import YoutubeClient
from ordered_set import OrderedSet
from contextlib import suppress
from time import sleep
from random import randint
import json


def load_data_from_file(path):
    with open(path) as file:
        data = json.load(file)
    return data or []


def save_as_json_to_file(data, path):
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)


if __name__ == '__main__':
    try:
        scope = ['https://www.googleapis.com/auth/youtube.readonly']
        fromInet = YoutubeClient(scope).fetch_links_to_all_videos()
        fromFile = load_data_from_file('urls.json')

        queue = OrderedSet(fromInet) - OrderedSet(fromFile)
        ready = OrderedSet()

        bot = Bot(getenv('TM_TOKEN'))
        channel = -1001283833543

        for msg in queue:
            with suppress(TelegramError):
                bot.sendMessage(channel, msg, disable_notification=False)
                ready.append(msg)
                sleep(randint(2, 5))

        lost = len(queue) - len(ready)
        if lost: print(f'Can\'t send {lost} of {len(queue)} videos')

        save_as_json_to_file(fromFile + list(ready), 'urls.json')

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

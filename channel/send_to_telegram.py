#!/usr/bin/env python3

from __init__ import *
from telegram import Bot, TelegramError
from googleapiclient.errors import HttpError
from youtube import YoutubeClient
from ordered_set import OrderedSet
from contextlib import suppress
from time import sleep
from random import randint
import config


def load_data_from_file(path):
    path = join(dirname(__file__), path)
    with open(path) as file:
        data = json.load(file)
    return data or []


def save_as_json_to_file(data, path):
    path = join(dirname(__file__), path)
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)


def send():
    try:
        scope = ['https://www.googleapis.com/auth/youtube']
        fromInet = YoutubeClient(scope).fetch_links_to_all_videos()
        fromFile = load_data_from_file('urls.json')

        queue = OrderedSet(fromInet) - OrderedSet(fromFile)
        ready = OrderedSet()

        env = config.load('config.prod.yml')
        bot = Bot(env['TM_TOKEN'])
        channel = env['CHANNEL']

        for msg in queue:
            with suppress(TelegramError):
                bot.sendMessage(channel, msg, disable_notification=True)
                ready.append(msg)
                sleep(randint(2, 5))

        lost = len(queue) - len(ready)
        save_as_json_to_file(fromFile + list(ready), 'urls.json')
        return f'Can\'t send {lost} of {len(queue)} videos' if lost else 'ok'

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))


if __name__ == '__main__':
    print(send())

#!/bin/python
import os

from telegram import Bot
from emoji import emojize
import yaml
import sys

path_to_config = os.path.join(os.path.dirname(__file__), '..', 'config.prod.yml')

with open(path_to_config) as file:
    config = yaml.load(file)

    chat = config['DEV_CHAT']
    msg = emojize(sys.argv[-1], use_aliases=True)
    Bot(config['TM_TOKEN']).sendMessage(chat, msg)

#!/bin/python

from telegram import Bot
from emoji import emojize
from init import load_config
import sys

config = load_config('../config.prod.yml')
chat = config['DEV_CHAT']
msg = emojize(sys.argv[-1], use_aliases=True)
Bot(config['TM_TOKEN']).sendMessage(chat, msg)

#!/usr/bin/env python3

# util to send messages to dev chat:
#   ./send_message.py "msg"

from __init__ import *
from telegram import Bot
from emoji import emojize
import config

conf = config.load('config.prod.yml')
chat = conf['DEV_CHAT']
msg = emojize(sys.argv[-1], use_aliases=True)
Bot(conf['TM_TOKEN']).sendMessage(chat, msg)

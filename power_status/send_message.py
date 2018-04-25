#!/usr/bin/env python3

from __init__ import *
from telegram import Bot
from emoji import emojize
import config

env = config.load('config.prod.yml')
chat = env['DEV_CHAT']
msg = emojize(sys.argv[-1], use_aliases=True)
Bot(env['TM_TOKEN']).sendMessage(chat, msg)

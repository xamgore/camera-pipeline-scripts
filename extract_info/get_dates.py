#!/usr/bin/env python3
import os
from pymediainfo import MediaInfo as media

sdcard = '/home/xi/sdcard/PRIVATE/AVCHD/BDMV/STREAM/'
movies = os.listdir(sdcard)

for f in movies:
    info = media.parse(sdcard + f).to_data()['tracks'][0]
    print(f'{f}:\t{info["recorded_date"]}\t{info["other_duration"][0]}')

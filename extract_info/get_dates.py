#!/usr/bin/env python3
import os
from pymediainfo import MediaInfo as media

sdcard = '/home/xi/sdcard/PRIVATE/AVCHD/BDMV/STREAM/'
movies = os.listdir(sdcard)

for f in movies:
    tracks = media.parse(sdcard + f).to_data()['tracks']
    info = [t for t in tracks if t['track_type'] == 'General'][0]
    print(f'{f}:\t{info["recorded_date"]}\t{info.get("other_duration", ["..."])[0]}')

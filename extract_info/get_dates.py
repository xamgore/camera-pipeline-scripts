#!/usr/bin/env python3
import os
import iso8601
from pymediainfo import MediaInfo as media
from datetime import datetime, timedelta

sdcard = '/home/xi/sdcard/PRIVATE/AVCHD/BDMV/STREAM/'
movies = os.listdir(sdcard)

for f in movies:
    tracks = media.parse(sdcard + f).to_data()['tracks']
    info = [t for t in tracks if t['track_type'] == 'General'][0]
    
    start    = info['recorded_date']
    duration = info.get('other_duration', ['...'])[0]
    
    t   = datetime.strptime( info.get('other_duration', ['', '', '', '00:00:00.000'])[3], '%H:%M:%S.%f' )
    end = iso8601.parse_date(start) + timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

    print(f'{f}:\t{start}\t{duration}\t{end}')

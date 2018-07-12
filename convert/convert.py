#!/usr/bin/env python3
# This utils takes a bunch of MTS files,
# concats them and runs audio normalizer.

import os
import ffmpeg
import argparse
from os.path import realpath
from datetime import datetime
from ffmpeg_normalize import FFmpegNormalize
from pymediainfo import MediaInfo as media
from iso8601 import parse_date


def get_default_name(path_to_mts_file):
    date = datetime.now()
    try:
        video_meta = media.parse(path_to_mts_file).to_data()
        track_info = [t for t in video_meta['tracks'] if t['track_type'] == 'General'][0]
        date = parse_date(track_info['recorded_date'])
    except:
        pass
    return date.strftime('%Y-%m-%d__%H-%M-%S.mp4')


parser = argparse.ArgumentParser(description='Convert a bunch of MTS files to a video with a normalized sound.')
parser.add_argument('path', nargs='+', type=argparse.FileType('r'), help='path to MTS file(s)')
parser.add_argument('-n', '--normalize', action='store_true', help='do audio normalization')
parser.add_argument('-o', nargs='?', metavar='FILE', help='output file name, record date by default')

args = parser.parse_args()

# Run concat via ffmpeg lib
output_file = args.o or get_default_name(args.path[0].name)
paths = '|'.join(realpath(p.name) for p in args.path)

err, output = (ffmpeg
               .input(f'concat:{paths}')
               .output(output_file, acodec='copy', vcodec='copy')
               .run(overwrite_output=True, quiet=True))

# If converted, normalize sound
if err != b'':
    print(output.decode())
elif args.normalize:
    os.environ["TMP"] = os.getcwd()
    normalizer = FFmpegNormalize(loudness_range_target=20, true_peak=0, audio_codec='aac', audio_bitrate='384k')
    normalizer.add_media_file(output_file, output_file)
    normalizer.run_normalization()

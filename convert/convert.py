#!/usr/bin/env python3
# This utils takes a bunch of MTS files,
# concats them and runs audio normalizer.

import os
import ffmpeg
import argparse
from os.path import realpath
from datetime import datetime as date
from ffmpeg_normalize import FFmpegNormalize

default_output_name = date.now().strftime('%Y-%m-%d_%H-%M-%S.mp4')

parser = argparse.ArgumentParser(description='Convert a bunch of MTS files to a video with a normalized sound.')
parser.add_argument('path', nargs='+', type=argparse.FileType('r'), help='path to MTS file(s)')
parser.add_argument('-n', '--normalize', action='store_true', help='do audio normalization')
parser.add_argument('-o', metavar='FILE', default=default_output_name, help='output file name, current date by default')
args = parser.parse_args()

paths = '|'.join(realpath(p.name) for p in args.path)
output_file = args.o

err, output = (ffmpeg
               .input(f'concat:{paths}')
               .output(output_file, acodec='copy', vcodec='copy')
               .run(overwrite_output=True, quiet=True))

if err != b'':
    print(output.decode())
elif args.normalize:
    os.environ["TMP"] = os.getcwd()
    normalizer = FFmpegNormalize(loudness_range_target=20, true_peak=0, audio_codec='aac', audio_bitrate='384k')
    normalizer.add_media_file(output_file, output_file)
    normalizer.run_normalization()

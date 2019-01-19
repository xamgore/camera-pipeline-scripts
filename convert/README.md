## Description

An util that concats `*.MTS` files and improves the audio loudness. It is a typical pipeline that we do with video lectures. It can be expressed in the following commands:

```bash
ffmpeg -i 'concat:0.MTS|1.MTS' -vcodec copy -acodec copy res.mp4
ffmpeg-normalize -v res.mp4 -c:a aac -b:a 384k -lrt 20 -tp 0 -o res.mp4
```

### Help

```
usage: convert.py [-h] [-n] [-o FILE] path [path ...]

Convert a bunch of MTS files to a video with a normalized sound.

positional arguments:
  path             path to MTS file(s)

optional arguments:
  -h, --help       show this help message and exit
  -n, --normalize  do audio normalization
  -o FILE          output file name, record date by default
```

### Examples

Handles relative paths:

```bash
./convert.py ~/video/5.MTS ../../6.MTS --normalize -o res.mp4
```

Output file name can be omitted, then the current time (like `2018-06-03__13-16-20.mp4`) is used:

```bash
./convert.py ~/video/5.MTS ../../6.MTS --normalize
```

The typcal example of usage is:

```bash
cd ~
./convert.py /sdcard/STREAM/{5,6,7,8}.MTS -o lecture.mp4
```

### Notes

The current directory is used as temprorary.

#### How to convert:

```bash
./au-camera-scripts/get_dates.py

python ~/au-camera-scripts/convert/convert.py movies/000{0..1}.MTS -o kek.mp4
```

#### fstab automount

```
LABEL=CAM_SD                                    /home/xi/sdcard exfat           nofail,noatime,x-systemd.device-timeout=1  0 2
```


#### Concat files

```bash
ffmpeg -i 'concat:00000.MTS|00001.MTS|00002.MTS|00003.MTS' -vcodec copy -ab 384 -acodec copy /home/xi/vid.mp4 -y
```

#### Generate thumbnails

```bash
ffmpeg -ss 3 -i sdcard/PRIVATE/AVCHD/BDMV/STREAM/00000.MTS -vf "select=gt(scene\,0.4)" -frames:v 5 -vsync vfr -vf fps=fps=1/600 
00000/%d.jpg
```

<!--### How to make it working

Register [OAuth 2.0 credentials](https://developers.google.com/youtube/registering_an_application#Create_OAuth2_Tokens) in Google account. Go to "Library", then enable "Youtube v3.0 API". Install python cli script:

```
$ sudo pip install --upgrade google-api-python-client progressbar2
$ git clone git@github.com:tokland/youtube-upload.git
$ python youtube-upload/bin/youtube-upload --help    

```-->

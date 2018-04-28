## About

This project describes, how to get some meaningful data from media files of SD-card.

##### Preparations

```bash
# Install dependencies
pacaur -S exfat-utils python-pymediainfo

# Insert SD-card and find its device id
sudo fdisk -l

# Assume, it is /dev/sdb1
sudo mount /dev/sdb1 ~/sdcard 
```

##### Explore the contents

```
sdcard
├── DCIM
│   ├── BACKUPAM.HST
│   ├── BACKUP.HST
│   ├── BACKUP.TMP
│   └── INDEX.DAT
└── PRIVATE
    └── AVCHD
        ├── AVCHDTN
        │   ├── THUMB.TDT
        │   └── THUMB.TID
        ├── BDMV
        │   ├── CLIPINF
        │   │   ├── 00000.CPI  <- clip info
        │   │   ├── 00001.CPI
        │   │   ├── 00002.CPI
        │   │   ├── 00003.CPI
        │   │   ├── 00004.CPI
        │   │   ├── 00005.CPI
        │   │   ├── 00006.CPI
        │   │   ├── 00007.CPI
        │   │   ├── 00008.CPI
        │   │   ├── 00009.CPI
        │   │   ├── 00010.CPI
        │   │   ├── 00011.CPI
        │   │   ├── 00012.CPI
        │   │   └── 00013.CPI
        │   ├── INDEX.BDM
        │   ├── MOVIEOBJ.BDM
        │   ├── PLAYLIST
        │   │   └── 00000.MPL
        │   └── STREAM
        │       ├── 00000.MTS  <- video files
        │       ├── 00001.MTS
        │       ├── 00002.MTS
        │       ├── 00003.MTS
        │       ├── 00004.MTS
        │       ├── 00005.MTS
        │       ├── 00006.MTS
        │       ├── 00007.MTS
        │       ├── 00008.MTS
        │       ├── 00009.MTS
        │       ├── 00010.MTS
        │       ├── 00011.MTS
        │       ├── 00012.MTS
        │       └── 00013.MTS
        └── PANA_EXT
            ├── BACKUP.CPI
            ├── BAK-S00.PDI
            └── BAK-S01.PDI
```

##### Grab info

Ok, let's use MediaInfo library, or rather its [wrapper](https://pymediainfo.readthedocs.io/en/latest/pymediainfo.html).

```python
from pymediainfo import MediaInfo as media
media.parse('PRIVATE/AVCHD/BDMV/STREAM/00000.MTS').to_data()
```

Result can be found in `examples/00000.MTS.json` folder.

##### Important fields

In my personal opinion, we need the following data from `tracks[track_type="General"]`:

```json
{
  "duration": "1589754.125000",
  "other_duration": [
    "26 min 29 s",
    "26 min 29 s 754 ms",
    "26 min 29 s",
    "00:26:29.754",
    "00:26:29:20",
    "00:26:29.754 (00:26:29:20)"
  ],
  
  "recorded_date": "2018-04-27 10:16:11+03:00",
  "file_last_modification_date": "UTC 2018-04-27 07:42:42",
  "file_last_modification_date__local": "2018-04-27 10:42:42"
}
```

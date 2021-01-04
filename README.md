# autoputio

Take all `.torrent` and `.magnet` files within a directory, add them to put.io
and delete the files.

## Usage

```
pip install --user -r requirements.txt
cp -r torrents.example torrents
python autoputio.py torrents
```

Optionally, a destination folder id can be given as the 2nd argument. All
torrents will be added to that folder.

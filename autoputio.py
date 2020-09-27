import sys
import glob
import os
import traceback

import putiopy

try:
    folder = sys.argv[1]
except IndexError:
    print(f"usage: {sys.argv[0]} FOLDER")
    sys.exit(1)

if 'PUTIO_OAUTH_TOKEN' not in os.environ:
    print(f"provide oauth token as $PUTIO_OAUTH_TOKEN")
    sys.exit(1)

client = putiopy.Client(os.environ['PUTIO_OAUTH_TOKEN'])


for torrent_file in glob.glob(folder + '/*.torrent'):
    print(f'adding {torrent_file}')
    try:
        client.Transfer.add_torrent(torrent_file)
        os.unlink(torrent_file)
    except:
        traceback.print_exc()


for magnet_file in glob.glob(folder + '/*.magnet'):
    with open(magnet_file) as f:
        url = f.read()

    print(f'adding url inside {magnet_file}')

    try:
        try:
            client.Transfer.add_url(url)
        except putiopy.ClientError as ex:
            if ex.type == 'Alreadyadded':
                print("already added")
            else:
                raise

        os.unlink(magnet_file)
    except:
        traceback.print_exc()

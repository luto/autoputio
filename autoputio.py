import sys
import glob
import os
import traceback

import putiopy


def add_torrents(client, folder):
    for torrent_file in glob.glob(folder + '/*.torrent'):
        print(f'adding {torrent_file}')
        try:
            client.Transfer.add_torrent(torrent_file)
            os.unlink(torrent_file)
        except:
            traceback.print_exc()


def add_magents(client, folder):
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


def main():
    try:
        folder = sys.argv[1]
    except IndexError:
        print(f"usage: {sys.argv[0]} FOLDER")
        sys.exit(1)

    try:
        access_token = os.environ['PUTIO_OAUTH_TOKEN']
    except LookupError:
        print(f"provide oauth token as $PUTIO_OAUTH_TOKEN")
        sys.exit(1)

    client = putiopy.Client(access_token)
    add_torrents(client, folder)
    add_magents(client, folder)


if __name__ == '__main__':
    main()

import sys
import glob
import os
import traceback

import putiopy


def add_torrents(client, folder, destination_id):
    for torrent_file in glob.glob(folder + '/*.torrent'):
        print(f'adding {torrent_file}')
        try:
            client.Transfer.add_torrent(torrent_file, destination_id)
            os.unlink(torrent_file)
        except:
            traceback.print_exc()


def add_magents(client, folder, destination_id):
    for magnet_file in glob.glob(folder + '/*.magnet'):
        with open(magnet_file) as f:
            url = f.read()

        print(f'adding url inside {magnet_file}')

        try:
            try:
                client.Transfer.add_url(url, destination_id)
            except putiopy.ClientError as ex:
                if ex.type == 'Alreadyadded':
                    print("already added")
                else:
                    raise

            os.unlink(magnet_file)
        except:
            traceback.print_exc()


def usage(err=''):
    print(f"usage: {sys.argv[0]} FOLDER [DESTINATION_FOLDER_ID]")
    print(f"provide oauth token as $PUTIO_OAUTH_TOKEN")
    if err:
        print(f'\n{err}')
    sys.exit(1)


def main():
    try:
        folder = sys.argv[1]
    except IndexError:
        usage('no source folder given')

    try:
        destination_id = int(sys.argv[2])
    except IndexError:
        destination_id = 0
    except ValueError:
        usage(f'destination id is not a number but: {sys.argv[2]}')

    try:
        access_token = os.environ['PUTIO_OAUTH_TOKEN']
    except LookupError:
        usage('no access token given')

    client = putiopy.Client(access_token)
    add_torrents(client, folder, destination_id)
    add_magents(client, folder, destination_id)


if __name__ == '__main__':
    main()

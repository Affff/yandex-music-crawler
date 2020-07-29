import json
import logging
import os
import shutil
import time
from pathlib import Path

from yandex_music.client import Client
from yandex_music.exceptions import Captcha

from __init__ import USER_LOGIN, USER_PASS

# Script uploads all user lists to 'json' folder.
# It also saves favorites list into 'favorites.json'.


def init_json_dir():
    if os.path.exists('json'):
        shutil.rmtree('json')
    Path('json').mkdir(parents=True, exist_ok=True)


def init_client():
    def process_captcha(captcha: Captcha) -> str:
        captcha.download('captcha.png')
        return input('Enter the number from picture: ')

    return Client.from_credentials(USER_LOGIN, USER_PASS, captcha_callback=process_captcha)


def save_tracks(title: str, tracks: list):
    data = {
        'tracks': [{
            'id': trackShort.track.id,
            'title': trackShort.track.title,
            'available': trackShort.track.available,
            'artists': [{
                'id': artist.id,
                'name': artist.name
            } for artist in trackShort.track.artists],
            'albums': [{
                'id': album.id,
                'title': album.title,
            } for album in trackShort.track.albums],
        } for trackShort in tracks]
    }
    with open('json/' + title + '.json', 'w') as outfile:
        json.dump(data, outfile)


logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

init_json_dir()

client = init_client()

user_lists = client.users_playlists_list()

user_lists = client.users_playlists([user_list.kind for user_list in user_lists])

for user_list in user_lists:
    print("Processing {} user list ({})".format(user_list.kind, user_list.title))
    save_tracks(user_list.title, user_list.tracks)
    time.sleep(5)

print("User lists processing done.")

favorites = client.users_likes_tracks()

print("Processing favorites...")

save_tracks("favorites", favorites.tracks)

print("done.")

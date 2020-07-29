import glob
import json

from __init__ import ALLOWED_USER_SUBLISTS

# Simple analyzer for user playlists JSON files
# Contains these checks:
# 1. All tracks in user list are in favorites;
# 2. All liked tracks are in some user playlist;
# 3. Every track included only once into the one user playlist skipping exceptions specified in ALLOWED_USER_SUBLISTS;

def load_json(file_name: str):
    with open(file_name, "r") as read_file:
        return json.load(read_file)


playlist_jsons = glob.glob("json/*.json")

playlists = {file_name[len("json/"):-len(".json")]: load_json(file_name) for file_name in playlist_jsons}

favorites = playlists["favorites"]
del playlists["favorites"]

favorites_ids = {track['id']: "favorites" for track in favorites['tracks']}
userlist_ids = {}

messages = []

for (file, playlist) in playlists.items():
    for track in playlist["tracks"]:
        track_id = track["id"]
        if track_id not in favorites_ids:
            messages.append("Found user list track missed in favorites: '{}' in '{}'".format(track["title"], file))
        if track_id in userlist_ids:
            initial_album = userlist_ids[track_id]
            if (file not in ALLOWED_USER_SUBLISTS or initial_album not in ALLOWED_USER_SUBLISTS[file]) \
                    and (initial_album not in ALLOWED_USER_SUBLISTS or file not in ALLOWED_USER_SUBLISTS[initial_album]):
                sign = '!!!' if file == initial_album else ''
                messages.append("{}Found duplicated track: '{}' in '{}', initial list is '{}'".format(sign,
                                                                                                      track[
                                                                                                          "title"],
                                                                                                      file,
                                                                                                      initial_album))
        else:
            userlist_ids[track_id] = file

diff = set(favorites_ids.keys()).difference(set(userlist_ids.keys()))
for track in favorites['tracks']:
    if track["id"] in diff:
        messages.append("Found liked track missed in user lists: '{}':{}".format(track["title"], track["id"]))

for message in sorted(messages):
    print(message)

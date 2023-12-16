import json
import os
from pprint import pprint


DATA_DIR = "data"

def handle_week(week_num: int):
    releases = []
    folder_path = f"{DATA_DIR}/{week_num}"
    for filename in os.listdir(folder_path):
        with open(f"{folder_path}/{filename}", 'r') as f:
            data = json.load(f)

        for item in data['results']:
            artists = item['artists']
            release_artists = []
            for artist in artists:
                release_artist = {
                    "id": artist['id'],
                    "name": artist['name'],
                    "url": artist['url']
                }
                release_artists.append(release_artist)

            remixers = item['remixers']
            release_remixers = []
            for remixer in remixers:
                release_remixer = {
                    "id": remixer['id'],
                    "name": remixer['name'],
                    "url": remixer['url']
                }
                release_remixers.append(release_remixer)
            release = {
                'artists': release_artists,
                'remixers': release_remixers,
                'catalog_number': item['catalog_number'],
                'new_release_date': item['new_release_date'],
                'publish_date': item['publish_date'],
                'updated': item['updated'],
                'upc': item['upc'],
                'label_name': item['label']['name'],
                'label_id': item['label']['id'],
                'desc': item['desc'],
                'release_id': item['id'],
                'release_name': item['name'],
                'release_url': item['url'],
                'track_count': item['track_count']
            }
            releases.append(release)
    with open(f"{folder_path}/full_week.json", 'w') as f:
        json.dump(releases, f, indent=4)

    pprint(releases)


def handle_week_tracks(week_num: int):
    folder_path = f"{DATA_DIR}/{week_num}"

    with open(f"{folder_path}/full_week.json", 'r') as f:
        releases = json.load(f)
    print(len(releases))
    tracks = []
    for release in releases:
        pass






if __name__ == "__main__":
    handle_week("09")
    # handle_week_tracks("09")
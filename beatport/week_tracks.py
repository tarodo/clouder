import json
import os
from pathlib import Path
from pprint import pprint
from environs import Env
import requests

from week_collector import DATA_DIR, BP_STYLES


TRACK_URL = "https://api.beatport.com/v4/catalog/releases/"

def collect_essential_week(raw_dir_path: Path):
    releases = []
    for week_page in raw_dir_path.iterdir():
        with open(week_page, 'r') as f:
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
    return releases


def handle_one_release(release: dict, raw_tracks_path: Path, bp_token: str):
    url = f"{TRACK_URL}{release.get('release_id')}/tracks"
    params = {
        "page": 1,
        "per_page": 100,
    }
    headers = {"Authorization": f"Bearer {bp_token}"}
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    tracks = r.json()
    pprint(tracks)
    with open(f"{raw_tracks_path}/{release.get('release_id')}.json", 'w') as f:
        json.dump(tracks, f, indent=4)


def handle_week_tracks(full_week_path: Path, raw_tracks_path: Path, bp_token: str):
    with open(full_week_path, 'r') as f:
        releases = json.load(f)

    for release in releases:
        handle_one_release(release, raw_tracks_path, bp_token)


def handle_week(week_num: int, style_id: int, bp_token: str):
    week_num = str(week_num).zfill(2)
    style_name = BP_STYLES.get(style_id)

    releases_path = Path(DATA_DIR) / style_name / week_num
    raw_dir_path = releases_path / "week_raw"
    full_week_path = releases_path / "full_week.json"

    raw_tracks_path = releases_path / "tracks_raw"
    os.makedirs(raw_tracks_path, exist_ok=True)

    releases = collect_essential_week(raw_dir_path)
    with open(full_week_path, 'w') as f:
        json.dump(releases, f, indent=4)

    handle_week_tracks(full_week_path, raw_tracks_path, bp_token)


if __name__ == "__main__":
    env = Env()
    env.read_env()
    bp_token = env.str("BP_TOKEN")
    handle_week(9, 1, bp_token)

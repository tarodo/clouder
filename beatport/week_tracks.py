import json
import os
from pathlib import Path
from pprint import pprint

from week_collector import DATA_DIR, BP_STYLES


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


def collect_whole_week(week_dir_path: Path):
    raw_dir_path = week_dir_path / "week_raw"
    result_path = week_dir_path / "full_week.json"

    releases = collect_essential_week(raw_dir_path)
    with open(result_path, 'w') as f:
        json.dump(releases, f, indent=4)


def handle_week(week_num: int, style_id: int):
    week_num = str(week_num).zfill(2)
    style_name = BP_STYLES.get(style_id)
    releases_path = Path(DATA_DIR) / style_name / week_num
    collect_whole_week(releases_path)


def handle_week_tracks(week_num: int):
    folder_path = f"{DATA_DIR}/{week_num}"

    with open(f"{folder_path}/full_week.json", 'r') as f:
        releases = json.load(f)
    print(len(releases))
    tracks = []
    for release in releases:
        pass


if __name__ == "__main__":
    handle_week(9, 1)

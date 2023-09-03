import logging
import csv
import requests
from pydantic import BaseModel

from playlists import PLAYLISTS, collect_playlist

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("weeker")


class BPRelease(BaseModel):
    bp_id: int
    name: str
    url: str
    release_date: str


def update_releases(url, params, headers, releases):
    logger.info(f"Try get: {url=}")
    if not url.startswith("https://"):
        url = f"https://{url}"
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    release_page = r.json()
    next_page = release_page['next']
    for release in release_page["results"]:
        releases.append(BPRelease(bp_id=release["id"], name=release["name"], url=release["url"], release_date=release["new_release_date"]))
    return next_page, dict(), releases


def collect_week(start_date: str, end_date: str, bp_token: str) -> list:
    logger.info(f"Start collect week from : {start_date} : to : {end_date} :: BP Token : {bp_token}")
    releases = []
    url = f"https://api.beatport.com/v4/catalog/releases/"
    params = {"genre_id": 1, "publish_date": f"{start_date}:{end_date}", "page": 1, "per_page": 100, "order_by": "-publish_date"}
    headers = {"Authorization": f"Bearer {bp_token}"}
    while url:
        url, params, releases = update_releases(url, params, headers, releases)
    return releases


if __name__ == "__main__":
    start = "2023-02-27"
    end = "2023-03-05"
    week_number = "09"
    bp_token = "TZ7vDyTuGmc8Pi3n7fmi4Na20SEsnz"
    logger.info(f"Start from {start} to {end} for {week_number} week")
    week_releases = collect_week(start, end, bp_token)

    with open(f"DNB_{week_number}.csv", 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for release in week_releases:
            line = [release.bp_id, release.name, release.release_date, release.url]
            csvwriter.writerow(line)

    playlists_id = PLAYLISTS.keys()
    for playlist_id in playlists_id:
        playlist = collect_playlist(playlist_id, bp_token)
        with open(f"DNB_{week_number}_{PLAYLISTS.get(playlist_id)}.csv", 'w', newline='', encoding='utf-8') as playlist_file:
            csvwriter = csv.writer(playlist_file)
            for track in playlist.tracks:
                line = [track.bp_id, track.name, track.isrc]
                csvwriter.writerow(line)

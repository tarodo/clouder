import csv
import json
import logging
import os
from environs import Env

import requests
from playlists import PLAYLISTS_DNB, collect_playlist
from pydantic import BaseModel
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("weeker")

DATA_DIR = "data"


class BPRelease(BaseModel):
    bp_id: int
    name: str
    url: str
    release_date: str


BP_STYLES = {
    1: "DNB",
}

RELEASE_WEEKS = {
    "09": ("2023-02-27", "2023-03-05"),
}


def update_releases(url, params, headers, releases, data_dir):
    logger.info(f"Try get: {url=}")
    if not url.startswith("https://"):
        url = f"https://{url}"
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    release_page = r.json()
    page_num = release_page['page'].replace("/", "_")
    with open(f"{data_dir}/weeker{page_num}.json", 'w') as f:
        json.dump(r.json(), f, indent=4)
    next_page = release_page["next"]
    for release in release_page["results"]:
        releases.append(
            BPRelease(
                bp_id=release["id"],
                name=release["name"],
                url=release["url"],
                release_date=release["new_release_date"],
            )
        )
    return next_page, dict(), releases


def collect_week(start_date: str, end_date: str, genre_id: int, bp_token: str, data_dir: Path) -> list:
    releases = []
    url = f"https://api.beatport.com/v4/catalog/releases/"
    params = {
        "genre_id": {genre_id},
        "publish_date": f"{start_date}:{end_date}",
        "page": 1,
        "per_page": 100,
        "order_by": "-publish_date",
    }
    headers = {"Authorization": f"Bearer {bp_token}"}
    data_dir = data_dir / "week_raw"
    os.makedirs(data_dir, exist_ok=True)
    while url:
        url, params, releases = update_releases(url, params, headers, releases, data_dir)
    return releases


def handle_dnb_week(week_number: int, style_id: int, bp_token: str):
    week_number = str(week_number).zfill(2)
    style_name = BP_STYLES.get(style_id)
    start = RELEASE_WEEKS.get(week_number)[0]
    end = RELEASE_WEEKS.get(week_number)[1]
    data_path = Path(DATA_DIR) / style_name / f"{week_number}"
    os.makedirs(data_path, exist_ok=True)

    logger.info(f"Start :: {style_name} ::  Week : {week_number} :: {start} : {end}")
    week_releases = collect_week(start, end, style_id, bp_token, data_path)

    file_path = data_path / f"{style_name}_{week_number}.csv"
    with open(f"{file_path}", "w", newline="", encoding="utf-8") as csvf:
        csvwriter = csv.writer(csvf)
        for release in week_releases:
            line = [release.bp_id, release.name, release.release_date, release.url]
            csvwriter.writerow(line)


if __name__ == "__main__":
    env = Env()
    env.read_env()
    bp_token = env.str("BP_TOKEN")

    handle_dnb_week(9, 1, bp_token)

    # playlists_id = PLAYLISTS_DNB.keys()
    # for playlist_id in playlists_id:
    #     playlist = collect_playlist(playlist_id, bp_token)
    #     with open(
    #         f"DNB_{week_number}_{PLAYLISTS_DNB.get(playlist_id)}.csv",
    #         "w",
    #         newline="",
    #         encoding="utf-8",
    #     ) as playlist_file:
    #         csvwriter = csv.writer(playlist_file)
    #         for track in playlist.tracks:
    #             line = [track.bp_id, track.name, track.isrc]
    #             csvwriter.writerow(line)

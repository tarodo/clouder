import json
import logging

import requests
from pydantic import BaseModel
from requests import HTTPError
from settings import bp_settings


logger = logging.getLogger("beatport")


class BPTrack(BaseModel):
    bp_id: int
    bp_playlist_id: int
    name: str
    authors: str
    isrc: str


class PlaylistIn(BaseModel):
    name: str
    tracks: list[BPTrack]


BASE_URL = "https://api.beatport.com/v4/my/playlists/"
PLAYLISTS = {
    1600521: "Melodic",
    1597656: "Party",
    1597654: "ReDrum",
    1597650: "Melancholy",
    1597645: "Hard",
}


def update_playlist_page(
        url: str, params: dict, headers: dict, tracks: list[BPTrack]
) -> tuple[str, dict, list[BPTrack]]:
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    playlist = r.json()
    next_page = playlist["next"]
    for playlist_pos in playlist["results"]:
        track = playlist_pos["track"]
        authors = ", ".join([artist["name"] for artist in track["artists"]])
        tracks.append(BPTrack(bp_playlist_id=playlist_pos["id"], bp_id=track["id"], name=track["name"], authors=authors, isrc=track["isrc"]))
    return next_page, dict(), tracks


def collect_playlist(playlist_id: int, bp_token: str) -> PlaylistIn:
    logger.info(f"Start collect playlist with ID : {playlist_id} :: BP Token : {bp_token}")
    playlist_name = PLAYLISTS[playlist_id]
    bp_tracks = []
    url = f"{BASE_URL}{playlist_id}/tracks/"
    params = {"page": 1, "per_page": 10}
    headers = {"Authorization": f"Bearer {bp_token}"}
    while url:
        url, params, bp_tracks = update_playlist_page(url, params, headers, bp_tracks)
    return PlaylistIn(name=playlist_name, tracks=bp_tracks)


def get_new_sp_playlist(name: str) -> dict | None:
    new_playlist_url = f"{bp_settings.spotify_service_url}/playlists/empty/{name}/"
    r = requests.post(new_playlist_url)
    try:
        r.raise_for_status()
    except HTTPError:
        logger.error(r.json())
        return
    return r.json()


async def collect_playlist_spotify(playlist: PlaylistIn) -> str:
    sp_playlist = get_new_sp_playlist(playlist.name)
    if sp_playlist is None:
        return "none"

    url = f"{bp_settings.spotify_service_url}/playlists/{sp_playlist['sp_id']}/tracks"
    tracks = playlist.tracks

    pack_size = 20
    parts = [
        tracks[i * pack_size : (i + 1) * pack_size]
        for i in range(len(tracks) // pack_size + 1)
    ]
    for part in parts:
        part = [track.model_dump() for track in part]
        tracks = {"tracks": part}
        r = requests.post(url, json=tracks)
        try:
            r.raise_for_status()
        except HTTPError as e:
            logger.error(r.json())
            return "none"
    return sp_playlist["url"]


def remove_tracks_from_playlist(playlist_id: int, tracks_id: list[int], bp_token: str):
    url = f"{BASE_URL}{playlist_id}/tracks/bulk/"
    data = {"item_ids": tracks_id}
    headers = {"Authorization": f"Bearer {bp_token}"}
    logger.info(f"Strat to delete : {tracks_id}")
    r = requests.delete(url, json=data, headers=headers)
    try:
        r.raise_for_status()
        return r.json()
    except HTTPError:
        logger.error(r.json(), exc_info=True)

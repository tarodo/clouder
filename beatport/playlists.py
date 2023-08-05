import requests
from pydantic import BaseModel
from requests import HTTPError
from settings import bp_settings


class BPTrack(BaseModel):
    name: str
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
) -> tuple[str, dict]:
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    playlist = r.json()
    next_page = playlist["next"]
    for playlist_pos in playlist["results"]:
        track = playlist_pos["track"]
        tracks.append(BPTrack(name=track["name"], isrc=track["isrc"]))
    return next_page, dict()


def collect_playlist(playlist_id: int, bp_token: str) -> PlaylistIn:
    playlist_name = PLAYLISTS[playlist_id]
    bp_tracks = []
    url = f"{BASE_URL}{playlist_id}/tracks/"
    params = {"page": 1, "per_page": 10}
    headers = {"Authorization": f"Bearer {bp_token}"}
    while url:
        url, params = update_playlist_page(url, params, headers, bp_tracks)
    return PlaylistIn(name=playlist_name, tracks=bp_tracks)


async def collect_playlist_spotify(playlist: PlaylistIn) -> str:
    url = f"{bp_settings.spotify_service_url}/playlists/"
    r = requests.post(url, data=playlist.model_dump_json())
    try:
        r.raise_for_status()
    except HTTPError:
        return "none"
    return r.json()["new_url"]

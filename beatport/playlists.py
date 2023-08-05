import requests
from pydantic import BaseModel


class BPTrack(BaseModel):
    name: str
    isrc: str


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


def collect_playlist(playlist_id: int, bp_token: str) -> list[BPTrack]:
    playlist_name = PLAYLISTS[playlist_id]
    bp_tracks = []
    url = f"{BASE_URL}{playlist_id}/tracks/"
    params = {"page": 1, "per_page": 10}
    headers = {"Authorization": f"Bearer {bp_token}"}
    while url:
        url, params = update_playlist_page(url, params, headers, bp_tracks)
    return bp_tracks
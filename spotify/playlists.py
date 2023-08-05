from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from models import PlaylistIn


def create_sp():
    scope = "playlist-modify-public"
    return Spotify(
        auth_manager=SpotifyOAuth(scope=scope, open_browser=False, show_dialog=True)
    )


def create_playlist(sp: Spotify, title: str) -> (str, str):
    try:
        print(sp.me())
        user_id = sp.me()["id"]
    except Exception:
        return None, None
    playlist = sp.user_playlist_create(user_id, title)
    return playlist["id"], playlist["external_urls"]["spotify"]


def create_playlist_from_bp(payload: PlaylistIn):
    sp = create_sp()
    playlist_id, playlist_url = create_playlist(sp, payload.name)
    return playlist_url


if __name__ == "__main__":
    sp = create_sp()
    sp.me()

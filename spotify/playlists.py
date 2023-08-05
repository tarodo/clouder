from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from models import PlaylistIn


def create_sp():
    client_credentials_manager = SpotifyClientCredentials()
    return Spotify(client_credentials_manager=client_credentials_manager)


def create_playlist(sp: Spotify, title: str) -> (str, str):
    print(sp.me())
    user_id = sp.me()["id"]
    playlist = sp.user_playlist_create(user_id, title)
    return playlist["id"], playlist["external_urls"]["spotify"]


def create_playlist_from_bp(payload: PlaylistIn):
    sp = create_sp()
    playlist_id, playlist_url = create_playlist(sp, payload.name)
    return playlist_url

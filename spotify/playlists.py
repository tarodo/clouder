import logging
import urllib.parse

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from models import PlaylistIn, SPTrack, SPPlaylist

logger = logging.getLogger("spotify")


def create_sp():
    scope = "playlist-modify-public"
    return Spotify(
        auth_manager=SpotifyOAuth(scope=scope, open_browser=False, show_dialog=True)
    )


def create_playlist(sp: Spotify, title: str) -> (str, str):
    try:
        user_id = sp.me()["id"]
    except Exception:
        return None, None
    playlist = sp.user_playlist_create(user_id, title)
    return playlist["id"], playlist["external_urls"]["spotify"]


def get_track_by_isrc(isrc: str, sp: Spotify = None) -> SPTrack | None:
    sp = sp if sp else create_sp()
    track_result = sp.search(q=f"isrc:{isrc}", type="track", limit=1)
    tracks = track_result["tracks"]["items"]
    if tracks:
        sp_track = tracks[0]
        title = sp_track["name"]
        track_id = sp_track["id"]
        url = sp_track["external_urls"]["spotify"]
        return SPTrack(name=title, sp_id=track_id, url=url)
    return None


def create_playlist_from_bp(payload: PlaylistIn):
    sp = create_sp()
    playlist_id, playlist_url = create_playlist(sp, payload.name)
    tracks_ids = []
    not_found = []
    for track in payload.tracks:
        sp_track = get_track_by_isrc(track.isrc, sp)
        if sp_track:
            tracks_ids.append(sp_track.sp_id)
        else:
            not_found.append(track)
    for track in not_found:
        search_str = f"{track.name} {track.authors}"
        logger.info(
            f"We couldn't find: {track=} || "
            f"https://open.spotify.com/search/{urllib.parse.quote(search_str)}"
        )
    pack_size = 100
    parts = [
        tracks_ids[i * pack_size : (i + 1) * pack_size]
        for i in range(len(tracks_ids) // pack_size + 1)
    ]
    for part in parts:
        sp.playlist_add_items(playlist_id, part)
    return playlist_url


def playlists_generator():
    """Generator of all playlists"""
    pass


def collect_playlists_by_mask(mask: str, sp: Spotify | None = None) -> list[SPPlaylist]:
    sp = sp if sp else create_sp()
    playlists_meta = sp.current_user_playlists(limit=50, offset=0)
    result = []
    total = playlists_meta["total"]
    playlists = playlists_meta["items"]
    for playlist in playlists:
        sp_playlist = SPPlaylist(sp_id=playlist["id"], url=playlist["external_urls"]["spotify"], name=playlist["name"])
        if sp_playlist.name.find("DNB") > 0:
            result.append(sp_playlist)
    return result

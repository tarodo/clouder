import logging
import re
from time import sleep

from spotipy import Spotify, SpotifyOAuth

from common import clear_artists_name
from models import (BeatportPlaylistModel, BeatportTrackModel,
                    SpotifyArtistModel, SpotifyTrackModel)

from datetime import date

logger = logging.getLogger("spotify")
logger.setLevel(logging.DEBUG)
handler_st = logging.StreamHandler()
handler_st.setLevel(logging.DEBUG)
strfmt = "[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
handler_st.setFormatter(formatter)
logger.addHandler(handler_st)


def create_sp():
    scope = "playlist-modify-public"
    return Spotify(auth_manager=SpotifyOAuth(scope=scope))


def create_search_for_bp(track: BeatportTrackModel):
    extended_type = "Extended" if "Extended" in track.remixed else ""
    artists = [artist.clear_name for artist in track.artists]
    search_str = f"{track.title} {' '.join(artists)} {extended_type}"
    search_str = search_str.replace("feat.", " ")
    search_str = search_str.strip()
    search_str = re.sub(r" +", " ", search_str)
    return search_str


def get_author(author_info: dict) -> SpotifyArtistModel:
    artist = SpotifyArtistModel(
        name=author_info["name"],
        clear_name=clear_artists_name(author_info["name"]),
        id=author_info["id"],
        url=author_info["external_urls"]["spotify"],
    )
    return artist


def get_track(track_info: dict) -> SpotifyTrackModel:
    track_date = None
    try:
        track_date = date.fromisoformat(track_info["album"]["release_date"])
    except ValueError as e:
        logger.error(e)
        logger.error(track_info)
    sp_track = SpotifyTrackModel(
        title=track_info["name"],
        id=track_info["id"],
        url=track_info["external_urls"]["spotify"],
        artists=[get_author(author) for author in track_info["artists"]],
        release_date=track_date,
    )
    return sp_track


def compare_with_bp(track_bp: BeatportTrackModel, track_sp: SpotifyTrackModel) -> bool:
    if track_bp.title != track_sp.title:
        return False

    for artist_bp in track_bp.artists:
        if artist_bp.clear_name not in [
            artist_sp.clear_name for artist_sp in track_sp.artists
        ]:
            return False

    return True


def search_track_for_bp(sp: Spotify, track_bp: BeatportTrackModel) -> SpotifyTrackModel:
    spoti_result = sp.search(q=create_search_for_bp(track_bp), type="track", limit=3)
    tracks = spoti_result["tracks"]["items"]
    tracks_sp = []
    for found_track in tracks:
        track_sp = get_track(found_track)
        if compare_with_bp(track_bp, track_sp):
            return track_sp
        tracks_sp.append(track_sp)

    artists_sp = [artist.name for artist in track_bp.artists]
    logger.info(
        f"Didn't find track :: '{track_bp.title} - {' '.join(artists_sp)}' :: id :: {track_bp.id}"
    )
    for track_sp in tracks_sp:
        logger.info(
            f"Track BP {track_bp.id} : found : {track_sp.title} :: "
            f"{[artist.name for artist in track_sp.artists]} :: {track_sp.url}"
        )


def create_playlist(sp: Spotify, title: str) -> (str, str):
    user_id = sp.me()["id"]
    playlist = sp.user_playlist_create(user_id, title)
    return playlist["id"], playlist["external_urls"]["spotify"]


def create_playlist_for_bp(sp: Spotify, playlist_bp: BeatportPlaylistModel) -> str:
    playlist_id, playlist_url = create_playlist(sp, playlist_bp.title)
    tracks_ids = []
    for track_bp in playlist_bp.tracks:
        track_sp = search_track_for_bp(sp, track_bp)
        sleep(0.2)
        if track_sp:
            tracks_ids.append(track_sp.id)
    pack_size = 100
    parts = [
        tracks_ids[i * pack_size : (i + 1) * pack_size]
        for i in range(len(tracks_ids) // pack_size + 1)
    ]
    for part in parts:
        sp.playlist_add_items(playlist_id, part)
    return playlist_url

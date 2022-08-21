import logging
import os
import shutil

from bs4 import BeautifulSoup

from common import clear_artists_name
from models import BeatportArtistModel, BeatportTrackModel, PlaylistModel

logger = logging.getLogger("beatport")
logger.setLevel(logging.INFO)
handler_st = logging.StreamHandler()
handler_st.setLevel(logging.INFO)
strfmt = "[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
handler_st.setFormatter(formatter)
logger.addHandler(handler_st)

PLAYLIST_DEFAULT_NAME = "Default Heap"


def get_playlist_data(file_path: str) -> BeautifulSoup:
    with open(file_path, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
    return soup


def check_file(file_path: str) -> bool:
    return bool(get_playlist_data(file_path).find(class_="library-playlist__info"))


def clear_dir(dir_path: str):
    shutil.rmtree(dir_path)
    os.makedirs(dir_path)


def find_playlist_name(soup: BeautifulSoup) -> str:
    playlist_name = soup.find(class_="library-playlist__name").text
    if not playlist_name:
        playlist_name = PLAYLIST_DEFAULT_NAME
    return playlist_name


def get_author(artist_soup: BeautifulSoup) -> BeatportArtistModel:
    artist_url: str = artist_soup["href"]
    artist_id = artist_url.split("/")[-1]
    artist = BeatportArtistModel(
        name=artist_soup.text,
        clear_name=clear_artists_name(artist_soup.text),
        id=artist_id,
        url=artist_url,
    )
    return artist


def get_track(track_soup: BeautifulSoup) -> BeatportTrackModel:
    title = track_soup.find(class_="track-title__primary").text
    remixed = track_soup.find(class_="track-title__remixed").text
    key = track_soup.find(class_="track-key").text
    bpm = track_soup.find(class_="track-bpm").text
    if bpm:
        bpm = int(bpm.split(" ")[0])
    track_url = track_soup.find(class_="track-title").find("a", href=True)["href"]
    track_id = track_url.split("/")[-1]
    artists = [
        get_author(soup) for soup in track_soup.find_all(class_="track-artists__artist")
    ]
    track = BeatportTrackModel(
        id=track_id,
        url=track_url,
        title=title,
        remixed=remixed,
        artists=artists,
        key=key,
        bpm=bpm,
    )
    logger.debug(f"Track :: {track}")
    return track


def find_count(soup: BeautifulSoup) -> int:
    playlist_detail = soup.find(class_="library-playlist__details").find_all("div")
    count = 0
    for detail in playlist_detail:
        one_detail = detail.find("p")
        if one_detail:
            one_detail = one_detail.text
            if "tracks" in one_detail:
                count = int(one_detail.split(" ")[0])
    return count


def find_tracks(soup: BeautifulSoup) -> list[BeatportTrackModel]:
    return [
        get_track(track_soup) for track_soup in soup.find_all(class_="tracks__item")
    ]


def collect_playlist(html_path: str) -> PlaylistModel:
    playlist_soup = get_playlist_data(html_path)
    playlist_name = find_playlist_name(playlist_soup)
    tracks_count = find_count(playlist_soup)
    tracks = find_tracks(playlist_soup)
    if len(tracks) != tracks_count:
        raise AssertionError(
            f"Full playlist '{playlist_name}' in '{html_path}' contains {tracks_count} tracks. "
            f"But in file - {len(tracks)}"
        )
    playlist = PlaylistModel(
        title=playlist_name, tracks_count=tracks_count, tracks=tracks
    )
    return playlist

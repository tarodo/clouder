import logging
import os
import shutil
from pathlib import Path

from bs4 import BeautifulSoup

from models import BeatportArtistModel, BeatportTrackModel, PlaylistModel

logger = logging.getLogger("beatport")
logger.setLevel(logging.DEBUG)
handler_st = logging.StreamHandler()
handler_st.setLevel(logging.DEBUG)
strfmt = "[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
handler_st.setFormatter(formatter)
logger.addHandler(handler_st)

PLAYLIST_DEFAULT_NAME = "Default Heap"
PLAYLIST_HTML_PATH = "../data/Playlists"


def get_playlist_data(file_path: str) -> BeautifulSoup:
    with open(file_path, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
    return soup


def check_file(file_path: str) -> bool:
    return bool(get_playlist_data(file_path).find(class_="library-playlist__info"))


def get_playlist_files(dir_path: str) -> list[str]:
    p = Path(PLAYLIST_HTML_PATH).glob("**/*")
    return [
        str(file_path)
        for file_path in p
        if file_path.is_file()
        and file_path.name.endswith(".html")
        and check_file(str(file_path))
    ]


def clear_dir(dir_path: str):
    shutil.rmtree(dir_path)
    os.makedirs(dir_path)


def find_playlist_name(soup: BeautifulSoup) -> str:
    playlist_name = soup.find(class_="library-playlist__name").text
    if not playlist_name:
        playlist_name = PLAYLIST_DEFAULT_NAME
    return playlist_name


def clear_artists_name(artist_name: str) -> str:
    return artist_name.strip().lower()


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
    title = track_soup.find(class_="track-title").text
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


def main():
    playlist_files = get_playlist_files(PLAYLIST_HTML_PATH)
    logger.info(f"Found playlists: {playlist_files}")
    try:
        playlists = [collect_playlist(one_file) for one_file in playlist_files]
    except AssertionError as e:
        logger.error(e.__str__())
    else:
        logger.info(
            f"Collected {len(playlists)} playlists "
            f"{[f'{pl.title} :: {pl.tracks_count} tracks' for pl in playlists]}"
        )
        # clear_dir(PLAYLIST_HTML_PATH)


if __name__ == "__main__":
    main()

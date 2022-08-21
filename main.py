import logging
import os
import shutil
from pathlib import Path
from environs import Env

from beatport import check_file, collect_playlist
from spotify import create_sp, create_playlist_for_bp

PLAYLIST_HTML_PATH = "data/Playlists"


logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
handler_st = logging.StreamHandler()
handler_st.setLevel(logging.DEBUG)
strfmt = "[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
handler_st.setFormatter(formatter)
logger.addHandler(handler_st)


def get_playlist_files(dir_path: str) -> list[str]:
    p = Path(dir_path).glob("**/*")
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


def main():
    env = Env()
    env.read_env()
    sp = create_sp()
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
        clear_dir(PLAYLIST_HTML_PATH)

        for playlist in playlists:
            new_playlist = create_playlist_for_bp(sp, playlist)
            logger.info(f"Create Spotify playlist :: {new_playlist}")


if __name__ == "__main__":
    main()
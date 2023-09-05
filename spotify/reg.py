import os

from playlists import create_sp

if not os.getenv("SPOTIPY_CLIENT_ID"):
    from environs import Env

    env = Env()
    env.read_env()


if __name__ == "__main__":
    sp = create_sp()
    sp.me()

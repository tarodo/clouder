import logging

from fastapi import Body, FastAPI, Path
from playlists import (create_one_playlist, create_playlist_from_bp,
                       get_track_by_isrc, handle_tracks_from_bp)

from models import BPTrack, BPTracks, PlaylistIn, SPPlaylist

app = FastAPI()

logger = logging.getLogger("spotify")
logger.setLevel(logging.DEBUG)
handler_st = logging.StreamHandler()
handler_st.setLevel(logging.DEBUG)
strfmt = "[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)
handler_st.setFormatter(formatter)
logger.addHandler(handler_st)


@app.get("/")
async def root():
    return {"message": "Hello Spotify"}


@app.post(
    "/playlists/empty/{playlist_name}/", response_model=SPPlaylist, status_code=200
)
def create_empty_playlist(playlist_name: str = Path(...)):
    playlist = create_one_playlist(playlist_name)
    return playlist


@app.post("/playlists/{playlist_id}/tracks")
def add_tracks_to_playlist(playlist_id: str = Path(...), tracks: BPTracks = Body(...)):
    result = handle_tracks_from_bp(playlist_id, tracks.tracks)
    return {"result": result}


@app.post("/playlists/")
def create_full_playlist(payload: PlaylistIn):
    playlist_url = create_playlist_from_bp(payload)
    return {"new_url": playlist_url}


@app.get("/findByISRC/{isrc}/")
def find_by_isrc(isrc: str = Path(...)):
    track = get_track_by_isrc(isrc)
    return {"track": track}

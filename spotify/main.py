from fastapi import FastAPI, Path
from playlists import create_playlist_from_bp, get_track_by_isrc

from models import PlaylistIn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Spotify"}


@app.post("/playlists/")
def create_user(payload: PlaylistIn):
    playlist_url = create_playlist_from_bp(payload)
    return {"new_url": playlist_url}


@app.get("/findByISRC/{isrc}/")
def find_by_isrc(isrc: str = Path(...)):
    track = get_track_by_isrc(isrc)
    return {"track": track}

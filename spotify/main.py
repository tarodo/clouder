from fastapi import FastAPI

from models import PlaylistIn
from playlists import create_playlist_from_bp

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Spotify"}


@app.post("/playlists/")
def create_user(payload: PlaylistIn):
    playlist_url = create_playlist_from_bp(payload)
    return {"new_url": playlist_url}

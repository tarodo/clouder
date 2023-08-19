import logging

from fastapi import FastAPI, Path, Query
from playlists import PlaylistIn, collect_playlist, collect_playlist_spotify, remove_tracks_from_playlist

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/playlists/{bp_playlist_id}")
async def create_user(
    bp_playlist_id: int = Path(..., gt=0), bp_token: str | None = Query(None)
):
    bp_playlist = collect_playlist(bp_playlist_id, bp_token)
    spotify_url = await collect_playlist_spotify(bp_playlist)
    return {"bp_playlist": bp_playlist, "spotify": spotify_url}


@app.post("/playlists/{bp_playlist_id}/clear/{bp_token}/")
async def clear_playlist(
    bp_playlist_id: int = Path(..., gt=0), bp_token: str = Path(...)
):
    bp_playlist = collect_playlist(bp_playlist_id, bp_token)
    tracks_id = [track.bp_playlist_id for track in bp_playlist.tracks]
    result = remove_tracks_from_playlist(playlist_id=bp_playlist_id, tracks_id=tracks_id, bp_token=bp_token)
    print(result)

from fastapi import FastAPI, Path, Query
from playlists import PlaylistIn, collect_playlist, collect_playlist_spotify

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

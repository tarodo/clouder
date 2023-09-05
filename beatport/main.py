import logging

from fastapi import FastAPI, Path, Query
from playlists import collect_playlist, collect_playlist_spotify, remove_tracks_from_playlist, PLAYLISTS_DNB

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/playlists/dnb/")
async def move_to_spotify_dnb(bp_token: str = Query(...)):
    new_sp_playlists = []
    for bp_playlist_id in PLAYLISTS_DNB.keys():
        bp_playlist = collect_playlist(bp_playlist_id, bp_token)
        spotify_url = await collect_playlist_spotify(bp_playlist)
        one_sp_playlist = {"name": bp_playlist.name, "sp_url": spotify_url}
        new_sp_playlists.append(one_sp_playlist)
    return {"playlists": new_sp_playlists}


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

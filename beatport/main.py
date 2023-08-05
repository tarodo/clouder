from fastapi import FastAPI, Path, Query

from playlists import collect_playlist

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/playlists/{bp_playlist_id}")
def create_user(
    bp_playlist_id: int = Path(..., gt=0), bp_token: str | None = Query(None)
):
    tracks = collect_playlist(bp_playlist_id, bp_token)
    return {"tracks": tracks}

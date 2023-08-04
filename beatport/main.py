import requests
import uvicorn
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/playlists/{bp_playlist_id}")
def create_user(
    bp_playlist_id: int = Path(..., gt=0), bp_token: str | None = Query(None)
):
    url = f"https://api.beatport.com/v4/my/playlists/{bp_playlist_id}/tracks/"
    params = {"page": 1, "per_page": 10}
    headers = {"Authorization": f"Bearer {bp_token}"}
    r = requests.get(url, params=params, headers=headers)
    playlist = r.json()

    return {
        "bp_token": bp_token,
        "bp_playlist_id": bp_playlist_id,
        "playlist": playlist,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

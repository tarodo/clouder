from pydantic import BaseModel


class BPTrack(BaseModel):
    name: str
    isrc: str


class PlaylistIn(BaseModel):
    name: str
    tracks: list[BPTrack]

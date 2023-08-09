from pydantic import BaseModel


class BPTrack(BaseModel):
    name: str
    authors: str
    isrc: str


class PlaylistIn(BaseModel):
    name: str
    tracks: list[BPTrack]


class SPPlaylist(BaseModel):
    name: str
    sp_id: str
    url: str


class SPTrack(BaseModel):
    name: str
    url: str
    sp_id: str

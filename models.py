from pydantic import BaseModel


class ArtistModel(BaseModel):
    name: str
    clear_name: str


class TrackModel(BaseModel):
    title: str
    artists: list[ArtistModel] | None


class PlaylistModel(BaseModel):
    title: str
    tracks_count: int
    tracks: list[TrackModel] | None


class BeatportArtistModel(ArtistModel):
    id: str
    url: str


class BeatportTrackModel(TrackModel):
    remixed: str
    id: str
    url: str
    artists: list[BeatportArtistModel] | None
    key: str | None
    bpm: int | None

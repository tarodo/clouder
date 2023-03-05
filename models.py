from datetime import date

from pydantic import BaseModel


class ArtistModel(BaseModel):
    name: str
    clear_name: str


class TrackModel(BaseModel):
    title: str


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


class BeatportPlaylistModel(BaseModel):
    title: str
    tracks_count: int
    tracks: list[BeatportTrackModel] | None


class SpotifyArtistModel(BeatportArtistModel):
    pass


class SpotifyTrackModel(TrackModel):
    id: str
    url: str
    artists: list[SpotifyArtistModel] | None
    release_date: date | None

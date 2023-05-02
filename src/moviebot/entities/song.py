from dataclasses import dataclass
import typing

SongNamedTuple = typing.NamedTuple(
    "SongNamedTuple",
    [
        ("songID", int),
        ("songName", str),
        ("composerID", int),
        ("movieID", int),
        ("songLength", int),
        ("ConnorsIncrediblyProfessionalAndPurelyObjectiveRating", str),
    ],
)


@dataclass
class Song:
    song_id: int
    song_name: str
    composer_id: int
    movie_id: int
    song_length: int
    connors_incredibly_professional_and_purely_objective_rating: str

    @staticmethod
    def from_named_tuple(data: SongNamedTuple) -> "Song":
        return Song(
            song_id=data.songID,
            song_name=data.songName,
            composer_id=data.composerID,
            movie_id=data.movieID,
            song_length=data.songLength,
            connors_incredibly_professional_and_purely_objective_rating=data.ConnorsIncrediblyProfessionalAndPurelyObjectiveRating,
        )

    def to_tuple(self):
        return (
            self.song_id,
            self.song_name,
            self.composer_id,
            self.movie_id,
            self.song_length,
            self.connors_incredibly_professional_and_purely_objective_rating,
        )

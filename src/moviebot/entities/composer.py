from dataclasses import dataclass
import typing

ComposerNamedTuple = typing.NamedTuple(
    "ComposerNamedTuple",
    [
        ("composerID", int),
        ("name", str),
        ("age", int),
        ("movieCount", int),
    ],
)


@dataclass
class Composer:
    composer_id: int
    name: str
    age: int
    movie_count: int

    @staticmethod
    def from_named_tuple(data: ComposerNamedTuple) -> "Composer":
        return Composer(
            composer_id=data.composerID,
            name=data.name,
            age=data.age,
            movie_count=data.movieCount,
        )

    def to_tuple(self):
        return (
            self.composer_id,
            self.name,
            self.age,
            self.movie_count,
        )

from dataclasses import dataclass
import typing

DirectorNamedTuple = typing.NamedTuple(
    "DirectorNamedTuple",
    [
        ("directorID", int),
        ("name", str),
        ("age", int),
    ],
)


@dataclass
class Director:
    director_id: int
    name: str
    age: int

    @staticmethod
    def from_named_tuple(data: DirectorNamedTuple) -> "Director":
        return Director(
            director_id=data.directorID,
            name=data.name,
            age=data.age,
        )

    def to_tuple(self):
        return (
            self.director_id,
            self.name,
            self.age,
        )

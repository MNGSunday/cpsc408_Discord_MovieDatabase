from dataclasses import dataclass
import typing

StudioNamedTuple = typing.NamedTuple(
    "StudioNamedTuple",
    [
        ("studioID", int),
        ("name", str),
        ("location", str),
    ],
)


@dataclass
class Studio:
    studio_id: int
    name: str
    location: str

    @staticmethod
    def from_named_tuple(data: StudioNamedTuple) -> "Studio":
        return Studio(
            studio_id=data.studioID,
            name=data.name,
            location=data.location,
        )

    def to_tuple(self):
        return (
            self.studio_id,
            self.name,
            self.location,
        )

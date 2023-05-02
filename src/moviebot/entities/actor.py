from dataclasses import dataclass
import typing


ActorNamedTuple = typing.NamedTuple(
    "ActorNamedTuple",
    [
        ("actorID", int),
        ("name", str),
        ("age", int),
        ("hotness", int),
        ("date", str),
    ],
)


@dataclass
class Actor:
    actor_id: int
    name: str
    age: int
    hotness: int
    date: str

    @staticmethod
    def from_named_tuple(data: ActorNamedTuple) -> "Actor":
        return Actor(
            actor_id=data.actorID,
            name=data.name,
            age=data.age,
            hotness=data.hotness,
            date=data.date,
        )

    def to_tuple(self):
        return (
            self.actor_id,
            self.name,
            self.age,
            self.hotness,
            self.date,
        )

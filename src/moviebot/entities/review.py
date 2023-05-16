from dataclasses import dataclass
import typing

ReviewNamedTuple = typing.NamedTuple(
    "ReviewNamedTuple",
    [
        ("reviewID", int),
        ("username", str),
        ("movieID", int),
        ("score", int),
        ("text", str),
        ("deleted", int),
    ],
)


@dataclass
class Review:
    review_id: int
    username: str
    movie_id: int
    score: int
    text: str
    deleted: bool

    @staticmethod
    def from_named_tuple(data: ReviewNamedTuple) -> "Review":
        return Review(
            review_id=data.reviewID,
            username=data.username,
            movie_id=data.movieID,
            score=data.score,
            text=data.text,
            deleted=data.deleted == 1,
        )

    def to_tuple(self):
        return (
            self.review_id,
            self.username,
            self.movie_id,
            self.score,
            self.text,
            self.deleted,
        )

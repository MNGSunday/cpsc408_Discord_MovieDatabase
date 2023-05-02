from dataclasses import dataclass
import typing

MovieNamedTuple = typing.NamedTuple(
    "MovieNamedTuple",
    [
        ("movieID", int),
        ("name", str),
        ("directorID", int),
        ("composerID", int),
        ("studioID", int),
        ("runtime", int),
        ("budget", int),
        ("grossProfit", int),
        ("criticScore", int),
        ("viewerScore", int),
        ("genre", str),
        ("year", int),
        ("nominatedForAward", bool),
        ("pSafeRating", str),
    ],
)


@dataclass
class Movie:
    movie_id: int
    name: str
    director_id: int
    composer_id: int
    studio_id: int
    runtime: int
    budget: int
    gross_profit: int
    critic_score: int
    viewer_score: int
    genre: str
    year: int
    nominated_for_award: bool
    p_safe_rating: str

    @staticmethod
    def from_named_tuple(data: MovieNamedTuple) -> "Movie":
        return Movie(
            movie_id=data.movieID,
            name=data.name,
            director_id=data.directorID,
            composer_id=data.composerID,
            studio_id=data.studioID,
            runtime=data.runtime,
            budget=data.budget,
            gross_profit=data.grossProfit,
            critic_score=data.criticScore,
            viewer_score=data.viewerScore,
            genre=data.genre,
            year=data.year,
            nominated_for_award=data.nominatedForAward,
            p_safe_rating=data.pSafeRating,
        )

    def to_tuple(self):
        return (
            self.movie_id,
            self.name,
            self.director_id,
            self.composer_id,
            self.studio_id,
            self.runtime,
            self.budget,
            self.gross_profit,
            self.critic_score,
            self.viewer_score,
            self.genre,
            self.year,
            self.nominated_for_award,
            self.p_safe_rating,
        )

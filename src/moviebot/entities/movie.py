from dataclasses import dataclass
import typing
from moviebot.entities.composer import Composer

from moviebot.entities.director import Director
from moviebot.entities.studio import Studio

MovieNamedTuple = typing.NamedTuple(
    "MovieNamedTuple",
    [
        ("movieID", int),
        ("movieName", str),
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
        ("directorName", str),
        ("directorAge", int),
        ("composerName", str),
        ("composerAge", int),
        ("composerMovieCount", int),
        ("studioName", str),
        ("studioLocation", str),
    ],
)


@dataclass
class Movie:
    movie_id: int
    name: str
    director: Director
    composer: Composer
    studio: Studio
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
        director = Director(
            director_id=data.directorID,
            name=data.directorName,
            age=data.directorAge,
        )

        composer = Composer(
            composer_id=data.composerID,
            name=data.composerName,
            age=data.composerAge,
            movie_count=data.composerMovieCount,
        )

        studio = Studio(
            studio_id=data.studioID,
            name=data.studioName,
            location=data.studioLocation,
        )

        return Movie(
            movie_id=data.movieID,
            name=data.movieName,
            director=director,
            composer=composer,
            studio=studio,
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
            self.director.director_id,
            self.composer.composer_id,
            self.studio.studio_id,
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

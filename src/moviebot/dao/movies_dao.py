from typing import Any, List

from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

from moviebot.dao.paginated_data import PaginatedData
from moviebot.entities import Movie
from moviebot.entities.movie import MovieNamedTuple


class MoviesDAO:
    def __init__(self, db: MySQLConnectionAbstract | PooledMySQLConnection):
        self.db = db

    def count(self) -> int:
        with self.db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Movies;")
            res = cursor.fetchone()
            if res is None:
                raise ValueError("No count returned")
            return res[0]

    def get_attributes(self) -> List[str]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM Movies LIMIT 1;")
            cursor.fetchall()
            return (
                [column[0] for column in cursor.description]
                if cursor.description
                else []
            )

    def get_by_id(self, movie_id: int) -> Movie | None:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM movies_with_director_composer_studio WHERE movieID = %s;",
                (movie_id,),
            )
            res = cursor.fetchone()
            if res is None:
                return None

            data = res[0] if isinstance(res, List) else res
            return Movie.from_named_tuple(MovieNamedTuple(*data))

    def list(self, offset: int = 0, limit: int = 5) -> PaginatedData[Movie]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM movies_with_director_composer_studio ORDER BY movieID LIMIT %s, %s;",
                (offset, limit),
            )
            return PaginatedData[Movie](
                data=[
                    Movie.from_named_tuple(movie_named_tuple)
                    for movie_named_tuple in cursor.fetchall()
                ],
                offset=offset,
                limit=limit,
                total=self.count(),
                paginate=self.list,
            )

    def get_random_movies(self, limit: int = 5) -> PaginatedData[Movie]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM movies_with_director_composer_studio ORDER BY RAND() LIMIT %s;",
                (limit,),
            )
            return PaginatedData[Movie](
                data=[
                    Movie.from_named_tuple(movie_named_tuple)
                    for movie_named_tuple in cursor.fetchall()
                ],
                offset=0,
                limit=limit,
                total=limit,
                paginate=lambda _, limit: self.get_random_movies(limit),
            )

    def get_movies(
        self,
        genre: str = None,
        min_budget: int = 0,
        max_budget: int = 2147483647,
        min_critic_score: int = 0,
        max_critic_score: int = 100,
        min_viewer_score: int = 0,
        max_viewer_score: int = 100,
        offset: int = 0,
        limit: int = 5,
    ) -> PaginatedData[Movie]:
        with self.db.cursor(named_tuple=True) as cursor:
            filters = [
                "budget >= %s",
                "budget <= %s",
                "criticScore >= %s",
                "criticScore <= %s",
                "viewerScore >= %s",
                "viewerScore <= %s",
            ]
            filter_values: List[Any] = [
                min_budget,
                max_budget,
                min_critic_score,
                max_critic_score,
                min_viewer_score,
                max_viewer_score,
            ]
            if genre is not None:
                filters.append("genre = %s")
                filter_values.append(genre)

            cursor.execute(
                f"SELECT COUNT(*) as total FROM movies_with_director_composer_studio WHERE {' AND '.join(filters)} ORDER BY movieID;",
                filter_values,
            )
            res = cursor.fetchone()
            if res is None:
                raise ValueError("No count returned")
            total = res.total

            cursor.execute(
                f"SELECT * FROM movies_with_director_composer_studio WHERE {' AND '.join(filters)} ORDER BY movieID;",
                filter_values,
            )
            return PaginatedData[Movie](
                data=[
                    Movie.from_named_tuple(movie_named_tuple)
                    for movie_named_tuple in cursor.fetchall()
                ],
                offset=offset,
                limit=limit,
                total=total,
                paginate=lambda offset, limit: self.get_movies(genre, offset, limit),
            )

    def get_movies_where_budget_greater_than_director_mean_budget(
        self, offset: int = 0, limit: int = 5
    ) -> PaginatedData[Movie]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT COUNT(*) as total FROM movies_with_director_composer_studio as m INNER JOIN ( SELECT directorID, directorName, AVG(grossProfit) as avgDirectorGrossProfit FROM movies_with_director_composer_studio as m GROUP BY directorID) as directorAvgGrossProfit ON m.directorID = directorAvgGrossProfit.directorID WHERE grossProfit >= avgDirectorGrossProfit;",
            )
            res = cursor.fetchone()
            if res is None:
                raise ValueError("No count returned")
            total = res.total

            cursor.execute(
                "SELECT m.* FROM movies_with_director_composer_studio as m INNER JOIN ( SELECT directorID, directorName, AVG(grossProfit) as avgDirectorGrossProfit FROM movies_with_director_composer_studio as m GROUP BY directorID) as directorAvgGrossProfit ON m.directorID = directorAvgGrossProfit.directorID WHERE grossProfit >= avgDirectorGrossProfit ORDER BY movieID LIMIT %s, %s;",
                (offset, limit),
            )
            return PaginatedData[Movie](
                data=[
                    Movie.from_named_tuple(movie_named_tuple)
                    for movie_named_tuple in cursor.fetchall()
                ],
                offset=offset,
                limit=limit,
                total=total,
                paginate=self.get_movies_where_budget_greater_than_director_mean_budget,
            )

    def create(
        self,
        name: str,
        director_id: int,
        composer_id: int,
        studio_id: int,
        runtime: int,
        budget: int,
        gross_profit: int,
        critic_score: int,
        viewer_score: int,
        genre: str,
        year: int,
        nominated_for_award: bool,
        p_safe_rating: str,
    ) -> Movie:
        with self.db.cursor() as cursor:
            cursor.execute(
                """INSERT INTO Movies (name, directorID, composerID, studioID, runtime, budget, grossProfit, criticScore, viewerScore, genre, year, nominatedForAward, pSafeRating)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                (
                    name,
                    director_id,
                    composer_id,
                    studio_id,
                    runtime,
                    budget,
                    gross_profit,
                    critic_score,
                    viewer_score,
                    genre,
                    year,
                    nominated_for_award,
                    p_safe_rating,
                ),
            )
            self.db.commit()
            if cursor.lastrowid is None:
                raise ValueError("Couldn't fetch last inserted movie")
            movie = self.get_by_id(cursor.lastrowid)
            if movie is None:
                raise ValueError("Couldn't fetch last inserted movie")
            return movie

    def update(self, movie_id: int, updated_values: dict) -> Movie:
        for key in updated_values.keys():
            if key not in self.get_attributes():
                raise ValueError(f"Invalid key {key}")

        set_string = ", ".join([f"{key} = %s" for key in updated_values.keys()])
        values = tuple(updated_values.values())

        with self.db.cursor() as cursor:
            cursor.execute(
                f"UPDATE Movies SET {set_string} WHERE movieID = %s;",
                values + (movie_id,),
            )
            self.db.commit()
            updated_movie = self.get_by_id(movie_id)
            if updated_movie is None:
                raise ValueError(f"Couldn't fetch updated movie with id {movie_id}")
            return updated_movie

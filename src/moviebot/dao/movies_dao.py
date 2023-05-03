from typing import List

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
        
    # def create(
    #     self,
    #     movie_id: int,
    #     name: str,
    #     director_id: int, 
    #     composer_id: int,
    #     studio_id: int,
    #     runtime: str,
    #     budget: int,
    #     gross_profit: int,
    #     critic_score: int,
    #     viewer_score: int,
    #     genre: str,
    #     year: int,
    #     nominated_for_award: int,
    #     parental_rating: str,
    # ) -> None:
    #     with self.db.cursor(named_tuple=True) as cursor:
    #         cursor.execute(
    #             "INSERT INTO Movies (MovieID, Name, DirectorID, ComposerID, StudioID, Runtime, Budget, Gross Profit, CriticScore, ViewerScore, Genre, Year, NominatedForAward, PSafeRating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
    #             (
    #                 movie_id,
    #                 name,
    #                 director_id,
    #                 composer_id,
    #                 studio_id,
    #                 runtime,
    #                 budget,
    #                 gross_profit,
    #                 critic_score,
    #                 viewer_score,
    #                 genre,
    #                 year,
    #                 nominated_for_award,
    #                 parental_rating,
    #             ),
    #         )
    #         self.db.commit()
    #         cursor.close()
            
    

    def get_by_id(self, movie_id: int) -> Movie | None:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM Movies WHERE movieID = %s;", (movie_id,))
            res = cursor.fetchone()
            if res is None:
                return None

            data = res[0] if isinstance(res, List) else res
            return Movie.from_named_tuple(MovieNamedTuple(*data))

    def list(self, offset: int = 0, limit: int = 5) -> PaginatedData[Movie]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM Movies ORDER BY movieID LIMIT %s, %s;", (offset, limit)
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

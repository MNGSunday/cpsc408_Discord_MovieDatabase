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

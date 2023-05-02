from typing import List

from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

from moviebot.dao.paginated_data import PaginatedData
from moviebot.entities.director import Director


class DirectorsDAO:
    def __init__(self, db: MySQLConnectionAbstract | PooledMySQLConnection):
        self.db = db

    def count(self) -> int:
        with self.db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Directors;")
            res = cursor.fetchone()
            if res is None:
                raise ValueError("No count returned")
            return res[0]

    def get_attributes(self) -> List[str]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM Directors LIMIT 1;")
            cursor.fetchall()
            return (
                [column[0] for column in cursor.description]
                if cursor.description
                else []
            )

    def list(self, offset: int = 0, limit: int = 5) -> PaginatedData[Director]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM Directors ORDER BY directorID LIMIT %s, %s;",
                (offset, limit),
            )
            return PaginatedData[Director](
                data=[
                    Director.from_named_tuple(director_named_tuple)
                    for director_named_tuple in cursor.fetchall()
                ],
                offset=offset,
                limit=limit,
                total=self.count(),
                paginate=self.list,
            )

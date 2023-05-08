from typing import List

from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

from moviebot.dao.paginated_data import PaginatedData
from moviebot.entities.director import Director, DirectorNamedTuple


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

    def get_by_id(self, director_id: int) -> Director | None:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM Directors WHERE directorID = %s;", (director_id,)
            )
            res = cursor.fetchone()
            if res is None:
                return None

            data = res[0] if isinstance(res, List) else res
            return Director.from_named_tuple(DirectorNamedTuple(*data))

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

    def create(
        self,
        name: str,
        age: int,
    ) -> Director:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "INSERT INTO Directors (name, age) VALUES (%s, %s);", (name, age)
            )
            self.db.commit()
            if cursor.lastrowid is None:
                raise ValueError("Last inserted director id is None")
            return Director(
                director_id=cursor.lastrowid,
                name=name,
                age=age,
            )

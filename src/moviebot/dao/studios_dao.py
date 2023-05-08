from typing import List

from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

from moviebot.dao.paginated_data import PaginatedData
from moviebot.entities.studio import Studio, StudioNamedTuple


class StudiosDAO:
    def __init__(self, db: MySQLConnectionAbstract | PooledMySQLConnection):
        self.db = db

    def count(self) -> int:
        with self.db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Studios;")
            res = cursor.fetchone()
            if res is None:
                raise ValueError("No count returned")
            return res[0]

    def get_attributes(self) -> List[str]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM Studios LIMIT 1;")
            cursor.fetchall()
            return (
                [column[0] for column in cursor.description]
                if cursor.description
                else []
            )

    def get_by_id(self, studio_id: int) -> Studio | None:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM Studios WHERE studioID = %s;", (studio_id,))
            res = cursor.fetchone()
            if res is None:
                return None

            data = res[0] if isinstance(res, List) else res
            return Studio.from_named_tuple(StudioNamedTuple(*data))

    def list(self, offset: int = 0, limit: int = 5) -> PaginatedData[Studio]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM Studios ORDER BY studioID LIMIT %s, %s;", (offset, limit)
            )
            return PaginatedData[Studio](
                data=[
                    Studio.from_named_tuple(studios_named_tuple)
                    for studios_named_tuple in cursor.fetchall()
                ],
                offset=offset,
                limit=limit,
                total=self.count(),
                paginate=self.list,
            )

    def create(self, name: str, location: str) -> Studio:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "INSERT INTO Studios (name, location) VALUES (%s, %s);",
                (name, location),
            )
            self.db.commit()
            if cursor.lastrowid is None:
                raise ValueError("Couldn't fetch last inserted studio")
            return Studio(
                studio_id=cursor.lastrowid,
                name=name,
                location=location,
            )

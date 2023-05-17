from typing import List

from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

from moviebot.dao.paginated_data import PaginatedData
from moviebot.entities.review import Review, ReviewNamedTuple


class ReviewsDAO:
    def __init__(self, db: MySQLConnectionAbstract | PooledMySQLConnection):
        self.db = db

    def count(self) -> int:
        with self.db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Reviews;")
            res = cursor.fetchone()
            if res is None:
                raise ValueError("No count returned")
            return res[0]

    def get_by_id(self, review_id: int) -> Review | None:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM Reviews WHERE reviewID = %s AND deleted = 0;",
                (review_id,),
            )
            res = cursor.fetchone()
            if res is None:
                return None

            data = res[0] if isinstance(res, List) else res
            return Review.from_named_tuple(ReviewNamedTuple(*data))

    def list(self, offset: int = 0, limit: int = 5) -> PaginatedData[Review]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM Reviews WHERE deleted = 0 ORDER BY reviewID LIMIT %s, %s;",
                (offset, limit),
            )
            return PaginatedData[Review](
                data=[
                    Review.from_named_tuple(review_named_tuple)
                    for review_named_tuple in cursor.fetchall()
                ],
                offset=offset,
                limit=limit,
                total=self.count(),
                paginate=self.list,
            )

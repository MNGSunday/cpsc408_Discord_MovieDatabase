from typing import List

import mysql.connector
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

    def create(self, username: str, movie_id: int, score: int, text: str):
        with self.db.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO Reviews (username, movieID, score, text, deleted) VALUES (%s, %s, %s, %s, %s);",
                    (username, movie_id, score, text, 0),
                )
                cursor.execute(
                    "INSERT INTO reviews_log VALUES (%s, %s, %s)",
                    (
                        username,
                        "Insert",
                        f"Inserted review with id: {cursor.lastrowid}",
                    ),
                )
                self.db.commit()
            except mysql.connector.Error as error:
                self.db.rollback()
                raise RuntimeError("Couldn't insert review and rolled back: ", error)
            if cursor.lastrowid is None:
                raise ValueError("Couldn't fetch last inserted movie review")
            return Review(
                review_id=cursor.lastrowid,
                username=username,
                movie_id=movie_id,
                score=score,
                text=text,
                deleted=False,
            )

    def update(self, username: str, review_id: int, new_text: str):
        with self.db.cursor() as cursor:
            try:
                cursor.execute(
                    "UPDATE Reviews SET text = %s WHERE reviewID = %s AND deleted = 0;",
                    (new_text, review_id),
                )
                cursor.execute(
                    "INSERT INTO reviews_log VALUES (%s, %s, %s)",
                    (
                        username,
                        "Update",
                        f"Updated review with id: {cursor.lastrowid}",
                    ),
                )
                self.db.commit()
            except mysql.connector.Error as error:
                self.db.rollback()
                raise RuntimeError("Couldn't update review and rolled back: ", error)
            updated_review = self.get_by_id(review_id)
            if updated_review is None:
                raise ValueError(f"Couldn't fetch updated review with id {review_id}")
            return updated_review

    def delete(self, username: str, review_id: int) -> None:
        with self.db.cursor() as cursor:
            try:
                cursor.execute(
                    "UPDATE Reviews SET deleted = 1 WHERE reviewID = %s AND deleted = 0;",
                    (review_id,),
                )
                cursor.execute(
                    "INSERT INTO reviews_log VALUES (%s, %s, %s)",
                    (
                        username,
                        "Delete",
                        f"Deleted review with id: {review_id}",
                    ),
                )
                self.db.commit()
            except mysql.connector.Error as error:
                self.db.rollback()
                raise RuntimeError("Couldn't delete review and rolled back: ", error)

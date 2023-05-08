from typing import List

from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

from moviebot.dao.paginated_data import PaginatedData
from moviebot.entities.composer import Composer, ComposerNamedTuple


class ComposersDAO:
    def __init__(self, db: MySQLConnectionAbstract | PooledMySQLConnection):
        self.db = db

    def count(self) -> int:
        with self.db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Composers;")
            res = cursor.fetchone()
            if res is None:
                raise ValueError("No count returned")
            return res[0]

    def get_attributes(self) -> List[str]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM Composers LIMIT 1;")
            cursor.fetchall()
            return (
                [column[0] for column in cursor.description]
                if cursor.description
                else []
            )

    def get_by_id(self, composer_id: int) -> Composer | None:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM Composers WHERE composerID = %s;", (composer_id,)
            )
            res = cursor.fetchone()
            if res is None:
                return None

            data = res[0] if isinstance(res, List) else res
            return Composer.from_named_tuple(ComposerNamedTuple(*data))

    def list(self, offset: int = 0, limit: int = 5) -> PaginatedData[Composer]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM Composers ORDER BY composerID LIMIT %s, %s;",
                (offset, limit),
            )
            return PaginatedData[Composer](
                data=[
                    Composer.from_named_tuple(composer_named_tuple)
                    for composer_named_tuple in cursor.fetchall()
                ],
                offset=offset,
                limit=limit,
                total=self.count(),
                paginate=self.list,
            )

    def create(self, name: str, age: int, movie_count: int) -> Composer:
        with self.db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Composers (name, age, movieCount) VALUES (%s, %s, %s);",
                (name, age, movie_count),
            )
            self.db.commit()

        if cursor.lastrowid is None:
            raise ValueError("Couldn't fetch last inserted composer")
        return Composer(
            composer_id=cursor.lastrowid, name=name, age=age, movie_count=movie_count
        )

    def update(self, composer_id: int, updated_values: dict) -> Composer:
        for key in updated_values.keys():
            if key not in self.get_attributes():
                raise ValueError(f"Invalid key {key}")

        set_string = ", ".join([f"{key} = %s" for key in updated_values.keys()])
        values = tuple(updated_values.values())

        with self.db.cursor() as cursor:
            cursor.execute(
                f"UPDATE Composers SET {set_string} WHERE composerID = %s;",
                values + (composer_id,),
            )
            self.db.commit()
            updated_composer = self.get_by_id(composer_id)
            if updated_composer is None:
                raise ValueError(
                    f"Couldn't fetch updated composer with id {composer_id}"
                )
            return updated_composer

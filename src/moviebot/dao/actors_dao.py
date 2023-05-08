from typing import List

from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

from moviebot.dao.paginated_data import PaginatedData
from moviebot.entities.actor import Actor, ActorNamedTuple


class ActorsDAO:
    def __init__(self, db: MySQLConnectionAbstract | PooledMySQLConnection):
        self.db = db

    def count(self) -> int:
        with self.db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Actors;")
            res = cursor.fetchone()
            if res is None:
                raise ValueError("No count returned")
            return res[0]

    def get_attributes(self) -> List[str]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM Actors LIMIT 1;")
            cursor.fetchall()
            return (
                [column[0] for column in cursor.description]
                if cursor.description
                else []
            )

    def get_by_id(self, actor_id: int) -> Actor | None:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM Actors WHERE actorID = %s;", (actor_id,))
            res = cursor.fetchone()
            if res is None:
                return None

            data = res[0] if isinstance(res, List) else res
            return Actor.from_named_tuple(ActorNamedTuple(*data))

    def list(self, offset: int = 0, limit: int = 5) -> PaginatedData[Actor]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM Actors ORDER BY actorID LIMIT %s, %s;", (offset, limit)
            )
            return PaginatedData[Actor](
                data=[
                    Actor.from_named_tuple(actor_named_tuple)
                    for actor_named_tuple in cursor.fetchall()
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
        hotness: int,
        date: str,
    ) -> Actor:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "INSERT INTO Actors (name, age, hotness, date) VALUES (%s, %s, %s, %s);",
                (name, age, hotness, date),
            )
            self.db.commit()
            if cursor.lastrowid is None:
                raise ValueError("Last inserted actor id is None")
            return Actor(
                actor_id=cursor.lastrowid,
                name=name,
                age=age,
                hotness=hotness,
                date=date,
            )

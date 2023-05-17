from typing import List

from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

from moviebot.dao.paginated_data import PaginatedData
from moviebot.entities.song import Song, SongNamedTuple


class SongsDAO:
    def __init__(self, db: MySQLConnectionAbstract | PooledMySQLConnection):
        self.db = db

    def count(self) -> int:
        with self.db.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Songs;")
            res = cursor.fetchone()
            if res is None:
                raise ValueError("No count returned")
            return res[0]

    def get_attributes(self) -> List[str]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM Songs LIMIT 1;")
            cursor.fetchall()
            return (
                [column[0] for column in cursor.description]
                if cursor.description
                else []
            )

    def get_by_id(self, song_id: int) -> Song | None:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM Songs WHERE songID = %s;", (song_id,))
            res = cursor.fetchone()
            if res is None:
                return None

            data = res[0] if isinstance(res, List) else res
            return Song.from_named_tuple(SongNamedTuple(*data))

    def list(self, offset: int = 0, limit: int = 5) -> PaginatedData[Song]:
        with self.db.cursor(named_tuple=True) as cursor:
            cursor.execute(
                "SELECT * FROM Songs ORDER BY songID LIMIT %s, %s;", (offset, limit)
            )
            return PaginatedData[Song](
                data=[
                    Song.from_named_tuple(song_named_tuple)
                    for song_named_tuple in cursor.fetchall()
                ],
                offset=offset,
                limit=limit,
                total=self.count(),
                paginate=self.list,
            )

    def create(
        self,
        name: str,
        composer_id: int,
        movie_id: int,
        length: int,
        connors_incredibly_professional_and_purely_objective_rating: str,
    ) -> Song:
        with self.db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Songs (songName, composerID, movieID, songLength, ConnorsIncrediblyProfessionalAndPurelyObjectiveRating, deleted) VALUES (%s, %s, %s, %s, %s, %s);",
                (
                    name,
                    composer_id,
                    movie_id,
                    length,
                    connors_incredibly_professional_and_purely_objective_rating,
                    0,
                ),
            )
            self.db.commit()
            if cursor.lastrowid is None:
                raise ValueError("Couldn't fetch last inserted song")
            return Song(
                song_id=cursor.lastrowid,
                song_name=name,
                composer_id=composer_id,
                movie_id=movie_id,
                song_length=length,
                connors_incredibly_professional_and_purely_objective_rating=connors_incredibly_professional_and_purely_objective_rating,
                deleted=False,
            )

    def update(self, song_id: int, updated_values: dict) -> Song:
        for key in updated_values.keys():
            if key not in self.get_attributes():
                raise ValueError(f"Invalid key {key}")

        set_string = ", ".join([f"{key} = %s" for key in updated_values.keys()])
        values = tuple(updated_values.values())

        with self.db.cursor() as cursor:
            cursor.execute(
                f"UPDATE Songs SET {set_string} WHERE songID = %s;",
                values + (song_id,),
            )
            self.db.commit()
            updated_song = self.get_by_id(song_id)
            if updated_song is None:
                raise ValueError(f"Couldn't fetch updated song with id {song_id}")
            return updated_song

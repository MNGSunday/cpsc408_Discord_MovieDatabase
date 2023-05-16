from discord.ext import commands
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection

from .dao import (
    ActorsDAO,
    ComposersDAO,
    DirectorsDAO,
    MoviesDAO,
    SongsDAO,
    StudiosDAO,
    ReviewsDAO,
)


class AbstractMovieBot(commands.Bot):
    def __init__(
        self, db: MySQLConnectionAbstract | PooledMySQLConnection, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.movies_dao = MoviesDAO(db)
        self.actors_dao = ActorsDAO(db)
        self.directors_dao = DirectorsDAO(db)
        self.composers_dao = ComposersDAO(db)
        self.songs_dao = SongsDAO(db)
        self.studios_dao = StudiosDAO(db)
        self.reviews_dao = ReviewsDAO(db)

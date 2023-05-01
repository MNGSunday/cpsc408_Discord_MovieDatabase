import discord
from discord.ext import commands
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from prettytable import PrettyTable

from .dao import MoviesDAO, ActorsDAO, DirectorsDAO


class MovieBot(commands.Bot):
    def __init__(
        self, db: MySQLConnectionAbstract | PooledMySQLConnection, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.movies_dao = MoviesDAO(db)
        self.actors_dao = ActorsDAO(db)
        self.directors_dao = DirectorsDAO(db)
        self._load_commands()

    def _load_commands(self):
        @self.command()
        async def test(ctx: commands.Context, table_name: str = None):
            await ctx.send(f"Test command ran with arg: {table_name}")

        list_command = discord.SlashCommandGroup(
            name="list", description="Lists records of what you want to see"
        )

        @list_command.command()
        async def movies(interaction: discord.Interaction):
            movie_attributes = self.movies_dao.get_attributes()
            movies = self.movies_dao.list()

            table = PrettyTable()
            table.field_names = movie_attributes
            table.add_rows(movies)

            await interaction.response.send_message(
                f"```\n{table}\n```",
                ephemeral=True,
            )

        @list_command.command()
        async def actors(interaction: discord.Interaction):
            actor_attributes = self.actors_dao.get_attributes()
            actors = self.actors_dao.list()

            table = PrettyTable()
            table.field_names = actor_attributes
            table.add_rows(actors)

            await interaction.response.send_message(
                f"```\n{table}\n```",
                ephemeral=True,
            )

        @list_command.command(description="Lists directors")
        async def directors(interaction: discord.Interaction):
            director_attributes = self.directors_dao.get_attributes()
            directors = self.directors_dao.list()

            table = PrettyTable()
            table.field_names = director_attributes
            table.add_rows(directors)

            await interaction.response.send_message(
                f"```\n{table}\n```",
                ephemeral=True,
            )

        self.add_application_command(list_command)

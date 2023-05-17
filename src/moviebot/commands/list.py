import discord
from discord.commands.options import option
from discord.ext import commands
from moviebot.abstract_moviebot import AbstractMovieBot
from moviebot.views.paginated_table_view import PaginatedTableView


class ListCommands(commands.Cog):
    def __init__(self, bot: AbstractMovieBot):
        self.bot = bot

    @commands.slash_command(
        name="list", description="Lists records of what you want to see"
    )
    @option(
        "entity",
        description="The entity you want to list",
        choices=[
            "movies",
            "actors",
            "directors",
            "composers",
            "songs",
            "studios",
            "reviews",
        ],
    )
    async def list_command(self, ctx: discord.ApplicationContext, entity: str):
        paginated_data = None

        if entity == "movies":
            paginated_data = self.bot.movies_dao.list()
        elif entity == "actors":
            paginated_data = self.bot.actors_dao.list()
        elif entity == "directors":
            paginated_data = self.bot.directors_dao.list()
        elif entity == "composers":
            paginated_data = self.bot.composers_dao.list()
        elif entity == "songs":
            paginated_data = self.bot.songs_dao.list()
        elif entity == "studios":
            paginated_data = self.bot.studios_dao.list()
        elif entity == "reviews":
            paginated_data = self.bot.reviews_dao.list()
        else:
            raise ValueError("Invalid entity")

        paginated_table_view = PaginatedTableView(paginated_data=paginated_data)
        await paginated_table_view.send(ctx)

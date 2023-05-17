import discord
from discord.commands.core import SlashCommandGroup
from discord.ext import commands
from moviebot.abstract_moviebot import AbstractMovieBot
from moviebot.views.paginated_table_view import PaginatedTableView


class RecommendMoviesCommands(commands.Cog):
    def __init__(self, bot: AbstractMovieBot):
        self.bot = bot

    recommend_movies_commands = SlashCommandGroup(
        "recommend_movies", "Get movie recommendations"
    )

    @recommend_movies_commands.command(name="random", description="Get random movies")
    async def random(self, ctx: discord.ApplicationContext, count: int):
        movies = self.bot.movies_dao.get_random_movies(limit=count)
        paginated_table_view = PaginatedTableView(paginated_data=movies)
        await paginated_table_view.send(ctx)

    @recommend_movies_commands.command(
        name="by_genre", description="Get movies by genre"
    )
    async def by_genre(self, ctx: discord.ApplicationContext, genre: str):
        movies = self.bot.movies_dao.get_movies_by_genre(genre)
        paginated_table_view = PaginatedTableView(paginated_data=movies)
        await paginated_table_view.send(ctx)

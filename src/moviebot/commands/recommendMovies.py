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
        name="by_filters", description="Get movies by filters"
    )
    async def by_filters(
        self,
        ctx: discord.ApplicationContext,
        genre: str = None,
        min_budget: int = None,
        max_budget: int = None,
        min_critic_score: int = None,
        max_critic_score: int = None,
        min_viewer_score: int = None,
        max_viewer_score: int = None,
    ):
        movies = self.bot.movies_dao.get_movies(
            genre=genre,
            min_budget=min_budget or 0,
            max_budget=max_budget or 2147483647,
            min_critic_score=min_critic_score or 0,
            max_critic_score=max_critic_score or 100,
            min_viewer_score=min_viewer_score or 0,
            max_viewer_score=max_viewer_score or 100,
        )

        paginated_table_view = PaginatedTableView(paginated_data=movies)
        await paginated_table_view.send(ctx)

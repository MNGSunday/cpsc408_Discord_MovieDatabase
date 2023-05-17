import discord
from discord.commands.options import option
from discord.ext import commands
from moviebot.abstract_moviebot import AbstractMovieBot
import pandas as pd


class ExportCommands(commands.Cog):
    def __init__(self, bot: AbstractMovieBot):
        self.bot = bot

    @commands.slash_command(
        name="export", description="Export records for some entity in a CSV file"
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
    async def export(self, ctx: discord.ApplicationContext, entity: str):
        data = None

        if entity == "movies":
            data = self.bot.movies_dao.list(limit=1000)
        elif entity == "actors":
            data = self.bot.actors_dao.list(limit=1000)
        elif entity == "directors":
            data = self.bot.directors_dao.list(limit=1000)
        elif entity == "composers":
            data = self.bot.composers_dao.list(limit=1000)
        elif entity == "songs":
            data = self.bot.songs_dao.list(limit=1000)
        elif entity == "studios":
            data = self.bot.studios_dao.list(limit=1000)
        elif entity == "reviews":
            data = self.bot.reviews_dao.list(limit=1000)
        else:
            raise ValueError("Invalid entity")

        if len(data.data) == 0:
            await ctx.response.send_message(
                f"No data to export for entity {entity}", ephemeral=True
            )
            return

        columns = list(data.data[0].__dict__.keys())
        data_tuples = [entity.to_tuple() for entity in data.data]
        df = pd.DataFrame(data_tuples, columns=columns)
        file_path = f"{entity}.csv"
        df.to_csv(file_path, index=False)
        await ctx.response.send_message(file=discord.File(file_path), ephemeral=True)

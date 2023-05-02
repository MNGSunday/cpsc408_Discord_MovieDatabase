import discord
from discord.commands.options import option
from prettytable import PrettyTable
from discord.ext import commands
from moviebot.abstract_moviebot import AbstractMovieBot


class ListCommands(commands.Cog):
    def __init__(self, bot: AbstractMovieBot):
        self.bot = bot

    @commands.slash_command(
        name="list", description="Lists records of what you want to see"
    )
    @option(
        "entity",
        description="The entity you want to list",
        choices=["movies", "actors", "directors", "composers", "songs", "studios"],
    )
    async def list_command(self, ctx: discord.ApplicationContext, entity: str):
        table = PrettyTable()

        if entity == "movies":
            table.field_names = self.bot.movies_dao.get_attributes()
            table.add_rows(self.bot.movies_dao.list())
        elif entity == "actors":
            table.field_names = self.bot.actors_dao.get_attributes()
            table.add_rows(self.bot.actors_dao.list())
        elif entity == "directors":
            table.field_names = self.bot.directors_dao.get_attributes()
            table.add_rows(self.bot.directors_dao.list())
        elif entity == "composers":
            table.field_names = self.bot.composers_dao.get_attributes()
            table.add_rows(self.bot.composers_dao.list())
        elif entity == "songs":
            table.field_names = self.bot.songs_dao.get_attributes()
            table.add_rows(self.bot.songs_dao.list())
        elif entity == "studios":
            table.field_names = self.bot.studios_dao.get_attributes()
            table.add_rows(self.bot.studios_dao.list())
        else:
            raise ValueError("Invalid entity")

        await ctx.response.send_message(f"```\n{table}\n```", ephemeral=True)

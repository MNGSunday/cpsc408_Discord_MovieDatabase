import discord
from prettytable import PrettyTable
from discord.ext import commands
from moviebot.abstract_moviebot import AbstractMovieBot


class ListCommands(commands.Cog):
    def __init__(self, bot: AbstractMovieBot):
        self.bot = bot

    list_command = discord.SlashCommandGroup(
        name="list", description="Lists records of what you want to see"
    )

    @list_command.command(description="Lists movies")
    async def movies(self, interaction: discord.Interaction):
        movie_attributes = self.bot.movies_dao.get_attributes()
        movies = self.bot.movies_dao.list()

        table = PrettyTable()
        table.field_names = movie_attributes
        table.add_rows(movies)

        await interaction.response.send_message(
            f"```\n{table}\n```",
            ephemeral=True,
        )

    @list_command.command(description="Lists actors")
    async def actors(self, interaction: discord.Interaction):
        actor_attributes = self.bot.actors_dao.get_attributes()
        actors = self.bot.actors_dao.list()

        table = PrettyTable()
        table.field_names = actor_attributes
        table.add_rows(actors)

        await interaction.response.send_message(
            f"```\n{table}\n```",
            ephemeral=True,
        )

    @list_command.command(description="Lists directors")
    async def directors(self, interaction: discord.Interaction):
        director_attributes = self.bot.directors_dao.get_attributes()
        directors = self.bot.directors_dao.list()

        table = PrettyTable()
        table.field_names = director_attributes
        table.add_rows(directors)

        await interaction.response.send_message(
            f"```\n{table}\n```",
            ephemeral=True,
        )

    @list_command.command(description="Lists composers")
    async def composers(self, interaction: discord.Interaction):
        composer_attributes = self.bot.composers_dao.get_attributes()
        composers = self.bot.composers_dao.list()

        table = PrettyTable()
        table.field_names = composer_attributes
        table.add_rows(composers)

        await interaction.response.send_message(
            f"```\n{table}\n```",
            ephemeral=True,
        )

    @list_command.command(description="Lists songs")
    async def songs(self, interaction: discord.Interaction):
        song_attributes = self.bot.songs_dao.get_attributes()
        songs = self.bot.songs_dao.list()

        table = PrettyTable()
        table.field_names = song_attributes
        table.add_rows(songs)

        await interaction.response.send_message(
            f"```\n{table}\n```",
            ephemeral=True,
        )

    @list_command.command(description="Lists studios")
    async def studios(self, interaction: discord.Interaction):
        studio_attributes = self.bot.studios_dao.get_attributes()
        studios = self.bot.studios_dao.list()

        table = PrettyTable()
        table.field_names = studio_attributes
        table.add_rows(studios)

        await interaction.response.send_message(
            f"```\n{table}\n```",
            ephemeral=True,
        )

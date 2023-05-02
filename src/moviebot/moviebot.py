import discord
from prettytable import PrettyTable

from moviebot.abstract_moviebot import AbstractMovieBot


class MovieBot(AbstractMovieBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_commands()

    def _load_commands(self):
        list_command = discord.SlashCommandGroup(
            name="list", description="Lists records of what you want to see"
        )

        @list_command.command(description="Lists movies")
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

        @list_command.command(description="Lists actors")
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

        @list_command.command(description="Lists composers")
        async def composers(interaction: discord.Interaction):
            composer_attributes = self.composers_dao.get_attributes()
            composers = self.composers_dao.list()

            table = PrettyTable()
            table.field_names = composer_attributes
            table.add_rows(composers)

            await interaction.response.send_message(
                f"```\n{table}\n```",
                ephemeral=True,
            )

        @list_command.command(description="Lists songs")
        async def songs(interaction: discord.Interaction):
            song_attributes = self.songs_dao.get_attributes()
            songs = self.songs_dao.list()

            table = PrettyTable()
            table.field_names = song_attributes
            table.add_rows(songs)

            await interaction.response.send_message(
                f"```\n{table}\n```",
                ephemeral=True,
            )

        @list_command.command(description="Lists studios")
        async def studios(interaction: discord.Interaction):
            studio_attributes = self.studios_dao.get_attributes()
            studios = self.studios_dao.list()

            table = PrettyTable()
            table.field_names = studio_attributes
            table.add_rows(studios)

            await interaction.response.send_message(
                f"```\n{table}\n```",
                ephemeral=True,
            )

        self.add_application_command(list_command)

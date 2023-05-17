import discord
from discord.commands.core import SlashCommandGroup
from discord.ext import commands
from moviebot.abstract_moviebot import AbstractMovieBot


class UpdateCommands(commands.Cog):
    def __init__(self, bot: AbstractMovieBot):
        self.bot = bot

    update_commands = SlashCommandGroup("update", "Update a record for some entity")

    @update_commands.command(name="song", description="Update a song")
    async def update_song(
        self,
        ctx: discord.ApplicationContext,
        song_id: int,
        name: str = None,
        composer_id: int = None,
        movie_id: int = None,
        length: int = None,
        connors_rating: str = None,
    ):
        updated_values = {}
        if name is not None:
            updated_values["songName"] = name
        if composer_id is not None:
            updated_values["composerID"] = composer_id
        if movie_id is not None:
            updated_values["movieID"] = movie_id
        if length is not None:
            updated_values["length"] = length
        if connors_rating is not None:
            updated_values[
                "ConnorsIncrediblyProfessionalAndPurelyObjectiveRating "
            ] = connors_rating

        song = self.bot.songs_dao.update(song_id=song_id, updated_values=updated_values)

        composer = self.bot.composers_dao.get_by_id(song.composer_id)
        movie = self.bot.movies_dao.get_by_id(song.movie_id)

        if composer is None or movie is None:
            raise ValueError("Song has invalid composer, movie foreign keys")

        embed = discord.Embed(title=song.song_name)
        embed.add_field(name="Composer", value=str(song.composer_id))
        embed.add_field(name="Movie", value=str(song.movie_id))
        embed.add_field(name="Length", value=str(song.song_length))
        embed.add_field(
            name="ConnorsIncrediblyProfessionalAndPurelyObjectiveRating",
            value=str(song.connors_incredibly_professional_and_purely_objective_rating),
        )
        await ctx.response.send_message(embed=embed, ephemeral=True)

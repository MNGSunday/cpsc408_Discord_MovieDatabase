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
        new_length: int,
    ):
        song = self.bot.songs_dao.update(song_id=song_id, new_song_length=new_length)

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

    @update_commands.command(name="review", description="Update a review")
    async def update_review(
        self,
        ctx: discord.ApplicationContext,
        review_id: int,
        new_text: str,
    ):
        review = self.bot.reviews_dao.update(review_id=review_id, new_text=new_text)

        movie = self.bot.movies_dao.get_by_id(review.movie_id)
        if movie is None:
            raise ValueError(f"Review has invalid movie foreign key")

        embed = discord.Embed()
        embed.add_field(name="Movie", value=movie.name, inline=False)
        embed.add_field(name="Score", value=str(review.score), inline=False)
        embed.add_field(name="Review", value=review.text, inline=False)
        await ctx.response.send_message(embed=embed, ephemeral=True)

import discord
from discord.commands.core import SlashCommandGroup
from discord.ext import commands
from moviebot.abstract_moviebot import AbstractMovieBot


class CreateCommands(commands.Cog):
    def __init__(self, bot: AbstractMovieBot):
        self.bot = bot

    create_commands = SlashCommandGroup("create", "Create a record for some entity")

    @create_commands.command(name="song", description="Create a song")
    async def create_song(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        composer_id: int,
        movie_id: int,
        length: int,
        connors_rating: str,
    ):
        song = self.bot.songs_dao.create(
            username=ctx.author.name,
            name=name,
            composer_id=composer_id,
            movie_id=movie_id,
            length=length,
            connors_incredibly_professional_and_purely_objective_rating=connors_rating,
        )

        embed = discord.Embed(title=song.song_name)
        embed.add_field(name="Composer", value=str(song.composer_id))
        embed.add_field(name="Movie", value=str(song.movie_id))
        embed.add_field(name="Length", value=str(song.song_length))
        embed.add_field(
            name="ConnorsIncrediblyProfessionalAndPurelyObjectiveRating",
            value=str(song.connors_incredibly_professional_and_purely_objective_rating),
        )

        await ctx.response.send_message("Song created", embed=embed, ephemeral=True)

    @create_commands.command(name="review", description="Write a review")
    async def create_review(
        self,
        ctx: discord.ApplicationContext,
        movie_id: int,
        score: int,
        text: str,
    ):
        review = self.bot.reviews_dao.create(
            username=ctx.user.name,
            movie_id=movie_id,
            score=score,
            text=text,
        )

        movie = self.bot.movies_dao.get_by_id(review.movie_id)
        if movie is None:
            raise ValueError(f"Review has invalid movie foreign key")

        embed = discord.Embed()
        embed.add_field(name="Movie", value=movie.name, inline=False)
        embed.add_field(name="Score", value=str(review.score), inline=False)
        embed.add_field(name="Review", value=review.text, inline=False)

        await ctx.response.send_message(embed=embed, ephemeral=True)

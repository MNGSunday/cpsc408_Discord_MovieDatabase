import discord
from discord.commands.core import SlashCommandGroup
from discord.ext import commands
from moviebot.abstract_moviebot import AbstractMovieBot


class DeleteCommands(commands.Cog):
    def __init__(self, bot: AbstractMovieBot):
        self.bot = bot

    delete_commands = SlashCommandGroup("delete", "Delete a record for some entity")

    @delete_commands.command(name="song", description="Delete a song")
    async def delete_song(
        self,
        ctx: discord.ApplicationContext,
        song_id: int,
    ):
        self.bot.songs_dao.delete(username=ctx.author.name, song_id=song_id)

        await ctx.response.send_message(
            f"Deleted song with id {song_id}", ephemeral=True
        )

    @delete_commands.command(name="review", description="Delete a review")
    async def delete_review(
        self,
        ctx: discord.ApplicationContext,
        review_id: int,
    ):
        self.bot.reviews_dao.delete(review_id=review_id)

        await ctx.response.send_message(
            f"Deleted review with id {review_id}", ephemeral=True
        )

import discord
from discord.commands.core import SlashCommandGroup
from discord.ext import commands
from moviebot.abstract_moviebot import AbstractMovieBot


class GetCommands(commands.Cog):
    def __init__(self, bot: AbstractMovieBot):
        self.bot = bot

    get_entity_commands = SlashCommandGroup(
        name="get", description="Create a record for some entity"
    )

    @get_entity_commands.command(name="movie", description="Get a movie given its id")
    async def get_movie(
        self,
        ctx: discord.ApplicationContext,
        movie_id: int,
    ):
        movie = self.bot.movies_dao.get_by_id(movie_id)
        if movie is None:
            await ctx.response.send_message(
                f"Movie with id `{movie_id}` does not exist", ephemeral=True
            )
            return

        embed = discord.Embed(title=movie.name)
        embed.add_field(name="Director", value=str(movie.director_id))
        embed.add_field(name="Composer", value=str(movie.composer_id))
        embed.add_field(name="Studio", value=str(movie.studio_id))
        embed.add_field(name="Runtime", value=f"{movie.runtime} min")
        embed.add_field(name="Budget", value=str(movie.budget))
        embed.add_field(name="Gross Profit", value=str(movie.gross_profit))
        embed.add_field(name="Critic Score", value=str(movie.critic_score))
        embed.add_field(name="Viewer Score", value=str(movie.viewer_score))
        embed.add_field(name="Genre", value=str(movie.genre))
        embed.add_field(name="Year", value=str(movie.year))
        embed.add_field(
            name="Nominated for Award",
            value="Yes" if movie.nominated_for_award else "No",
        )
        embed.add_field(name="P Safe Rating", value=str(movie.p_safe_rating))
        await ctx.response.send_message(embed=embed, ephemeral=True)

    @get_entity_commands.command(
        name="actor", description="Get an actor given their id"
    )
    async def get_actor(
        self,
        ctx: discord.ApplicationContext,
        actor_id: int,
    ):
        actor = self.bot.actors_dao.get_by_id(actor_id)
        if actor is None:
            await ctx.response.send_message(
                f"Actor with id `{actor_id}` does not exist", ephemeral=True
            )
            return

        embed = discord.Embed(title=actor.name)
        embed.add_field(name="Age", value=str(actor.age))
        embed.add_field(name="Hotness", value=str(actor.hotness))
        embed.add_field(name="Would I date them", value=actor.date)
        await ctx.response.send_message(embed=embed, ephemeral=True)

    @get_entity_commands.command(
        name="director", description="Get a director given their id"
    )
    async def get_director(
        self,
        ctx: discord.ApplicationContext,
        director_id: int,
    ):
        director = self.bot.directors_dao.get_by_id(director_id)
        if director is None:
            await ctx.response.send_message(
                f"Director with id `{director_id}` does not exist", ephemeral=True
            )
            return

        embed = discord.Embed(title=director.name)
        embed.add_field(name="Age", value=str(director.age))

        await ctx.response.send_message(embed=embed, ephemeral=True)

    @get_entity_commands.command(
        name="composer", description="Get a composer given their id"
    )
    async def get_composer(
        self,
        ctx: discord.ApplicationContext,
        composer_id: int,
    ):
        composer = self.bot.composers_dao.get_by_id(composer_id)
        if composer is None:
            await ctx.response.send_message(
                f"Composer with id `{composer_id}` does not exist", ephemeral=True
            )
            return

        embed = discord.Embed(title=composer.name)
        embed.add_field(name="Age", value=str(composer.age))
        embed.add_field(name="Movie Count", value=str(composer.movie_count))
        await ctx.response.send_message(embed=embed, ephemeral=True)

    @get_entity_commands.command(name="song", description="Get a song given its id")
    async def get_song(
        self,
        ctx: discord.ApplicationContext,
        song_id: int,
    ):
        song = self.bot.songs_dao.get_by_id(song_id)
        if song is None:
            await ctx.response.send_message(
                f"Song with id `{song_id}` does not exist", ephemeral=True
            )
            return

        embed = discord.Embed(title=song.song_name)
        embed.add_field(name="Composer", value=str(song.composer_id))
        embed.add_field(name="Movie", value=str(song.movie_id))
        embed.add_field(name="Length", value=str(song.song_length))
        embed.add_field(
            name="ConnorsIncrediblyProfessionalAndPurelyObjectiveRating",
            value=str(song.connors_incredibly_professional_and_purely_objective_rating),
        )
        await ctx.response.send_message(embed=embed, ephemeral=True)

    @get_entity_commands.command(name="studio", description="Get a studio given its id")
    async def get_studio(
        self,
        ctx: discord.ApplicationContext,
        studio_id: int,
    ):
        studio = self.bot.studios_dao.get_by_id(studio_id)
        if studio is None:
            await ctx.response.send_message(
                f"Studio with id `{studio_id}` does not exist", ephemeral=True
            )
            return

        embed = discord.Embed(title=studio.name)
        embed.add_field(name="Location", value=str(studio.location))
        await ctx.response.send_message(embed=embed, ephemeral=True)

import discord
from discord.commands.core import SlashCommandGroup
from discord.ext import commands
from moviebot.abstract_moviebot import AbstractMovieBot


class CreateCommands(commands.Cog):
    def __init__(self, bot: AbstractMovieBot):
        self.bot = bot

    create_commands = SlashCommandGroup("create", "Create a record for some entity")

    @create_commands.command(name="movie", description="Create a movie")
    async def create_movie(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        director_id: int,
        composer_id: int,
        studio_id: int,
        runtime: int,
        budget: int,
        gross_profit: int,
        critic_score: int,
        viewer_score: int,
        genre: str,
        year: int,
        nominated_for_award: bool,
        p_safe_rating: str,
    ):
        movie = self.bot.movies_dao.create(
            name=name,
            director_id=director_id,
            composer_id=composer_id,
            studio_id=studio_id,
            runtime=runtime,
            budget=budget,
            gross_profit=gross_profit,
            critic_score=critic_score,
            viewer_score=viewer_score,
            genre=genre,
            year=year,
            nominated_for_award=nominated_for_award,
            p_safe_rating=p_safe_rating,
        )

        director = self.bot.directors_dao.get_by_id(movie.director_id)
        composer = self.bot.composers_dao.get_by_id(movie.composer_id)
        studio = self.bot.studios_dao.get_by_id(movie.studio_id)

        if director is None or composer is None or studio is None:
            raise ValueError(
                "Movie has invalid director, composer, studio foreign keys"
            )

        embed = discord.Embed(title=movie.name)
        embed.add_field(name="Director", value=director.name)
        embed.add_field(name="Composer", value=composer.name)
        embed.add_field(name="Studio", value=studio.name)
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
        await ctx.response.send_message("Created movie", embed=embed, ephemeral=True)

    @create_commands.command(name="actor", description="Create an actor")
    async def create_actor(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        age: int,
        hotness: int,
        date: str,
    ):
        actor = self.bot.actors_dao.create(
            name=name, age=age, hotness=hotness, date=date
        )

        embed = discord.Embed(title=actor.name)
        embed.add_field(name="Age", value=str(actor.age))
        embed.add_field(name="Hotness", value=str(actor.hotness))
        embed.add_field(name="Would I date them", value=actor.date)
        await ctx.response.send_message("Actor created", embed=embed, ephemeral=True)

    @create_commands.command(name="director", description="Create a director")
    async def create_director(
        self,
        ctx: discord.ApplicationContext,
        name: str,
        age: int,
    ):
        director = self.bot.directors_dao.create(name=name, age=age)

        embed = discord.Embed(title=director.name)
        embed.add_field(name="Age", value=str(director.age))

        await ctx.response.send_message("Director created", embed=embed, ephemeral=True)

    @create_commands.command(name="composer", description="Create a composer")
    async def create_composer(
        self, ctx: discord.ApplicationContext, name: str, age: int, movie_count: int
    ):
        composer = self.bot.composers_dao.create(
            name=name, age=age, movie_count=movie_count
        )

        embed = discord.Embed(title=composer.name)
        embed.add_field(name="Age", value=str(composer.age))
        embed.add_field(name="Movie Count", value=str(composer.movie_count))

        await ctx.response.send_message(embed=embed, ephemeral=True)

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

    @create_commands.command(name="studio", description="Create a studio")
    async def create_studio(
        self, ctx: discord.ApplicationContext, name: str, location: str
    ):
        studio = self.bot.studios_dao.create(name=name, location=location)

        embed = discord.Embed(title=studio.name)
        embed.add_field(name="Location", value=str(studio.location))

        await ctx.response.send_message("Studio created", embed=embed, ephemeral=True)

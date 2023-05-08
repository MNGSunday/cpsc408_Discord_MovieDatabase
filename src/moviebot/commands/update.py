import discord
from discord.commands.core import SlashCommandGroup
from discord.ext import commands
from moviebot.abstract_moviebot import AbstractMovieBot


class UpdateCommands(commands.Cog):
    def __init__(self, bot: AbstractMovieBot):
        self.bot = bot

    update_commands = SlashCommandGroup("update", "Update a record for some entity")

    @update_commands.command(name="movie", description="Update a movie")
    async def update_movie(
        self,
        ctx: discord.ApplicationContext,
        movie_id: int,
        name: str = None,
        director_id: int = None,
        composer_id: int = None,
        studio_id: int = None,
        runtime: int = None,
        budget: int = None,
        gross_profit: int = None,
        critic_score: int = None,
        viewer_score: int = None,
        genre: str = None,
        year: int = None,
        nominated_for_award: bool = None,
        p_safe_rating: str = None,
    ):
        updated_values = {}
        if name is not None:
            updated_values["name"] = name
        if director_id is not None:
            updated_values["directorID"] = director_id
        if composer_id is not None:
            updated_values["composerID"] = composer_id
        if studio_id is not None:
            updated_values["studioID"] = studio_id
        if runtime is not None:
            updated_values["runtime"] = runtime
        if budget is not None:
            updated_values["budget"] = budget
        if gross_profit is not None:
            updated_values["grossProfit"] = gross_profit
        if critic_score is not None:
            updated_values["criticScore"] = critic_score
        if viewer_score is not None:
            updated_values["viewerScore"] = viewer_score
        if genre is not None:
            updated_values["genre"] = genre
        if year is not None:
            updated_values["year"] = year
        if nominated_for_award is not None:
            updated_values["nominatedForAward"] = nominated_for_award
        if p_safe_rating is not None:
            updated_values["pSafeRating"] = p_safe_rating

        movie = self.bot.movies_dao.update(
            movie_id=movie_id, updated_values=updated_values
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
        await ctx.response.send_message("Updated movie", embed=embed, ephemeral=True)

    @update_commands.command(name="actor", description="Update an actor")
    async def update_actor(
        self,
        ctx: discord.ApplicationContext,
        actor_id: int,
        name: str = None,
        age: int = None,
        hotness: int = None,
        date: str = None,
    ):
        updated_values = {}
        if name is not None:
            updated_values["name"] = name
        if age is not None:
            updated_values["age"] = age
        if hotness is not None:
            updated_values["hotness"] = hotness
        if date is not None:
            updated_values["date"] = date

        actor = self.bot.actors_dao.update(
            actor_id=actor_id, updated_values=updated_values
        )

        embed = discord.Embed(title=actor.name)
        embed.add_field(name="Age", value=str(actor.age))
        embed.add_field(name="Hotness", value=str(actor.hotness))
        embed.add_field(name="Date", value=str(actor.date))
        await ctx.response.send_message("Updated actor", embed=embed, ephemeral=True)

    @update_commands.command(name="director", description="Update a director")
    async def update_director(
        self,
        ctx: discord.ApplicationContext,
        director_id: int,
        name: str = None,
        age: int = None,
    ):
        updated_values = {}
        if name is not None:
            updated_values["name"] = name
        if age is not None:
            updated_values["age"] = age

        director = self.bot.directors_dao.update(
            director_id=director_id, updated_values=updated_values
        )

        embed = discord.Embed(title=director.name)
        embed.add_field(name="Age", value=str(director.age))

        await ctx.response.send_message("Updated director", embed=embed, ephemeral=True)

    @update_commands.command(name="composer", description="Update a composer")
    async def update_composer(
        self,
        ctx: discord.ApplicationContext,
        composer_id: int,
        name: str = None,
        age: int = None,
        movie_count: int = None,
    ):
        updated_values = {}
        if name is not None:
            updated_values["name"] = name
        if age is not None:
            updated_values["age"] = age
        if movie_count is not None:
            updated_values["movieCount"] = movie_count

        composer = self.bot.composers_dao.update(
            composer_id=composer_id, updated_values=updated_values
        )

        embed = discord.Embed(title=composer.name)
        embed.add_field(name="Age", value=str(composer.age))
        embed.add_field(name="Movie Count", value=str(composer.movie_count))
        await ctx.response.send_message(embed=embed, ephemeral=True)

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

    @update_commands.command(name="studio", description="Update a studio")
    async def update_studio(
        self,
        ctx: discord.ApplicationContext,
        studio_id: int,
        name: str = None,
        location: str = None,
    ):
        updated_values = {}
        if name is not None:
            updated_values["name"] = name
        if location is not None:
            updated_values["location"] = location

        studio = self.bot.studios_dao.update(
            studio_id=studio_id, updated_values=updated_values
        )

        embed = discord.Embed(title=studio.name)
        embed.add_field(name="Location", value=str(studio.location))
        await ctx.response.send_message(embed=embed, ephemeral=True)

import discord
from discord.commands.options import option
from prettytable import PrettyTable
from discord.ext import commands
from moviebot.abstract_moviebot import AbstractMovieBot
from moviebot.dao.paginated_data import PaginatedData


class PaginatedTableView(discord.ui.View):
    def __init__(self, paginated_data: PaginatedData):
        super().__init__()
        self.paginated_data = paginated_data

    async def send(self, ctx: discord.ApplicationContext):
        self._update_buttons()
        self.message = await ctx.response.send_message(
            f"```\n{self._get_table()}\n```", view=self, ephemeral=True
        )

    @discord.ui.button(label="|<", style=discord.ButtonStyle.secondary)
    async def first_button(
        self, _: discord.ui.Button, interaction: discord.Interaction
    ):
        self.paginated_data = self.paginated_data.get_first_page()
        self._update_buttons()
        await self._update_message(interaction)

    @discord.ui.button(label="<", style=discord.ButtonStyle.secondary)
    async def previous_button(
        self, _: discord.ui.Button, interaction: discord.Interaction
    ):
        self.paginated_data = self.paginated_data.get_previous_page()
        self._update_buttons()
        await self._update_message(interaction)

    @discord.ui.button(label=">", style=discord.ButtonStyle.secondary)
    async def next_button(self, _: discord.ui.Button, interaction: discord.Interaction):
        self.paginated_data = self.paginated_data.get_next_page()
        self._update_buttons()
        await self._update_message(interaction)

    @discord.ui.button(label=">|", style=discord.ButtonStyle.secondary)
    async def last_button(self, _: discord.ui.Button, interaction: discord.Interaction):
        self.paginated_data = self.paginated_data.get_last_page()
        self._update_buttons()
        await self._update_message(interaction)

    def _update_buttons(self):
        self.first_button.disabled = not self.paginated_data.previous_page_exists()
        self.previous_button.disabled = not self.paginated_data.previous_page_exists()
        self.next_button.disabled = not self.paginated_data.next_page_exists()
        self.last_button.disabled = not self.paginated_data.next_page_exists()

    async def _update_message(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            content=f"```\n{self._get_table()}\n```", view=self
        )

    def _get_table(self):
        table = PrettyTable()

        if len(self.paginated_data.data) > 0:
            table.field_names = self.paginated_data.data[0].__dict__.keys()

        table.add_rows([entity.to_tuple() for entity in self.paginated_data.data])

        return table


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
        paginated_data = None

        if entity == "movies":
            paginated_data = self.bot.movies_dao.list()
        elif entity == "actors":
            paginated_data = self.bot.actors_dao.list()
        elif entity == "directors":
            paginated_data = self.bot.directors_dao.list()
        elif entity == "composers":
            paginated_data = self.bot.composers_dao.list()
        elif entity == "songs":
            paginated_data = self.bot.songs_dao.list()
        elif entity == "studios":
            paginated_data = self.bot.studios_dao.list()
        else:
            raise ValueError("Invalid entity")

        paginated_table_view = PaginatedTableView(paginated_data=paginated_data)
        await paginated_table_view.send(ctx)

import discord
from prettytable import PrettyTable
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

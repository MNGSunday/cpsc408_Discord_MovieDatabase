from discord.ext import commands


class MovieBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_commands()

    def _load_commands(self):
        @self.command()
        async def test(ctx: commands.Context, table_name: str = None):
            await ctx.send(f"Test command ran with arg: {table_name}")

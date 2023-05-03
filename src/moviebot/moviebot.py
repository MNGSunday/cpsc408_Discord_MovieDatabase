from moviebot.abstract_moviebot import AbstractMovieBot
from moviebot.commands.get import GetCommands
from moviebot.commands.list import ListCommands


class MovieBot(AbstractMovieBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_commands()

    def _load_commands(self):
        cogs = [
            ListCommands(self),
            GetCommands(self),
        ]
        for cog in cogs:
            self.add_cog(cog)

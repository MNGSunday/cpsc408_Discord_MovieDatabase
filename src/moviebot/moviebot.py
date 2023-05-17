from moviebot.abstract_moviebot import AbstractMovieBot
from moviebot.commands.create import CreateCommands
from moviebot.commands.delete import DeleteCommands
from moviebot.commands.get import GetCommands
from moviebot.commands.list import ListCommands
from moviebot.commands.update import UpdateCommands


class MovieBot(AbstractMovieBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_commands()

    def _load_commands(self):
        cogs = [
            ListCommands(self),
            GetCommands(self),
            CreateCommands(self),
            UpdateCommands(self),
            DeleteCommands(self),
        ]
        for cog in cogs:
            self.add_cog(cog)

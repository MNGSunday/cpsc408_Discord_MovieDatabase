from moviebot.abstract_moviebot import AbstractMovieBot
from moviebot.commands.list import ListCommands


class MovieBot(AbstractMovieBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_commands()

    def _load_commands(self):
        self.add_cog(ListCommands(self))

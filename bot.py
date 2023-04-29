import discord
from dotenv import load_dotenv
import os
import sys
from moviebot import MovieBot

load_dotenv()

discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
if discord_bot_token is None:
    print("DISCORD_BOT_TOKEN is not set")
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = True

bot = MovieBot(command_prefix="!", intents=intents)

bot.run(discord_bot_token)

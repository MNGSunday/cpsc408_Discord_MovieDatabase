import discord
from dotenv import load_dotenv
import os
import sys
import mysql.connector
from moviebot import MovieBot

load_dotenv()

discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
if discord_bot_token is None:
    print("DISCORD_BOT_TOKEN is not set")
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = True

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "cpsc408",
    "auth_plugin": "mysql_native_password",
    "database": "MovieBot",
}

with mysql.connector.connect(**DB_CONFIG) as db:
    bot = MovieBot(db=db, command_prefix="!", intents=intents)

    bot.run(discord_bot_token)

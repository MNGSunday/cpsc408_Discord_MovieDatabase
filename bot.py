import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import sys

load_dotenv()

discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
if discord_bot_token is None:
    print("DISCORD_BOT_TOKEN is not set")
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Bot is ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.command()
async def test(ctx: commands.Context, table_name: str = None):
    await ctx.send(f"Test command ran with arg: {table_name}")


bot.run(discord_bot_token)

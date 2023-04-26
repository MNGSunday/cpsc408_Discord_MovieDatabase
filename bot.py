import discord
from discord.ext import commands
from dotenv import load_dotenv
import os


@commands.command()
async def test(ctx: commands.Context, arg: str = None):
    await ctx.send(f"Test command ran with arg: {arg}")


def main():
    load_dotenv()

    discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
    if discord_bot_token is None:
        print("DISCORD_BOT_TOKEN is not set")
        return

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    bot_commands = [test]

    for bot_command in bot_commands:
        bot.add_command(bot_command)

    bot.run(discord_bot_token)


if __name__ == "__main__":
    main()

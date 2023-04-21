import discord
from dotenv import load_dotenv
import os


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")


def main():
    load_dotenv()

    discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
    if discord_bot_token is None:
        print("DISCORD_BOT_TOKEN is not set")
        return

    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(discord_bot_token)


if __name__ == "__main__":
    main()

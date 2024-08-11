import discord
import os

from dotenv import load_dotenv


def run_client():

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith("$hello"):
            await message.channel.send("Hello!")

    load_dotenv()
    discord_token = os.getenv("DISCORD_TOKEN")
    print(discord_token)
    client.run(discord_token)

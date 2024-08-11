import discord
import os
import re

from dotenv import load_dotenv


class DiscordClient:

    message_pattern = r"(?i)\b(?:Смотрим|Смотрю)\b\s+([A-Za-z\s\'\:]+)\s+(\d{4})"

    def __init__(self):
        load_dotenv()
        self.discord_private_token = os.getenv("DISCORD_TOKEN")
        self.debug_message_channel = os.getenv("DEBUG_MESSAGE_CHANNEL")
        self.cinema_channel_name = os.getenv("CINEMA_CHANNEL_NAME")
        self.cinema_channel_id = None
        print(self.discord_private_token)

        intents = discord.Intents.default()
        intents.message_content = True

        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_ready():
            await self.__on_ready()

        @self.client.event
        async def on_message(message):
            await self.__on_message(message)

    def run(self):
        self.client.run(self.discord_private_token)

    async def __on_ready(self):
        print(f"We have logged in as {self.client.user}")
        channels = self.client.get_all_channels()
        # get channel id by name
        for channel in channels:
            if channel.name == self.cinema_channel_name:
                self.cinema_channel_id = channel.id
                async for message in channel.history(limit=99999):
                    if self.analyse_message(message):
                        await message.add_reaction("👍")

    async def __on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith("$hello"):
            await message.channel.send("Hello! " + str(message.channel.id))

        if message.content.startswith("$clear_reactions"):
            channel = self.client.get_channel(self.cinema_channel_id)
            async for message in channel.history(limit=99999):
                for reaction in message.reactions:
                    if reaction.me:
                        print("My reaction")
                        print(message.content)
                        # await reaction.remove(self.client.user)

    def analyse_message(self, message):
        match = re.search(self.message_pattern, message.content)
        if match:
            print(f"Matched: {message.content}")
            print(match.groups())
            print(match.group(1))
            print(match.group(2))
            print("----")
            return True
        return False

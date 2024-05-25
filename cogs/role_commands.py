import disnake
from disnake.ext import commands
import asyncio

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_time = {}
        self.message_time = {}

    async def add_voice_time(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for guild in self.bot.guilds:
                for member in guild.members:
                    if member.voice and member.voice.channel:
                        if member.id not in self.voice_time:
                            self.voice_time[member.id] = 0
                        self.voice_time[member.id] += 1
            await asyncio.sleep(60)

    async def add_message_time(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    async for message in channel.history(limit=None):
                        if message.author.id not in self.message_time:
                            self.message_time[message.author.id] = 0
                        self.message_time[message.author.id] += 1
            await asyncio.sleep(60)

def setup(bot):
    bot.add_cog(Ranking(bot))

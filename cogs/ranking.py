import disnake
from disnake.ext import commands
import config

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = config.CHANNEL_ID

    @commands.command()
    async def set_channel(self, ctx, channel: disnake.TextChannel):
        self.channel_id = channel.id
        await ctx.send(f"Канал установлен: {channel.mention}")

    async def send_to_channel(self, message):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send(message)

    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        await self.send_to_channel(f"**{message.author.name}**: {message.content}")

def setup(bot):
    bot.add_cog(Ranking(bot))
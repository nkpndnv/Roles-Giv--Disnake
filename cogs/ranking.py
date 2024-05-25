import disnake
from disnake.ext import commands
import asyncio

voice_time = {}
message_time = {}

rank_roles = {
    1007975444693405873: {"voice_exp": 10, "text_exp": 5}, # Зомби
    1007974554779533372: {"voice_exp": 20, "text_exp": 10}, # Глаз
    1007975692463517718: {"voice_exp": 40, "text_exp": 20}, # Скелет
    1007975658175086662: {"voice_exp": 60, "text_exp": 40}, # Демон
    1145253606732349471: {"voice_exp": 80, "text_exp": 80}, # Стена плоти
    1007976053643431959: {"voice_exp": 100, "text_exp": 160}, # Мимик
    1007977167382118472: {"voice_exp": 120, "text_exp": 320}, # Виверна
    1209427732681981992: {"voice_exp": 140, "text_exp": 640}, # Клон каламиитас
    1145251337525805066: {"voice_exp": 160, "text_exp": 800}, # Плантера
    1209427733902401566: {"voice_exp": 180, "text_exp": 900}, # Голиаф
    1145253064941506651: {"voice_exp": 200, "text_exp": 1000}, # Императтрица света
    1145252178701852682: {"voice_exp": 220, "text_exp": 1100}, # Голем
    1007976560466329600: {"voice_exp": 240, "text_exp": 1200}, # Рыброн
    1209878068756226048: {"voice_exp": 260, "text_exp": 1300}, # Мутант
    1209428390189334539: {"voice_exp": 280, "text_exp": 1400}, # Мерзость
    1007977472559677490: {"voice_exp": 300, "text_exp": 1500}, # Культист
    1007977789376446507: {"voice_exp": 320, "text_exp": 1600}, # Лунный лорд
    1145252726343729172: {"voice_exp": 340, "text_exp": 1700}, # Провиденс
    1209877394740088833: {"voice_exp": 360, "text_exp": 1800}, # Полтергаст
    1209427734779002880: {"voice_exp": 380, "text_exp": 1900}, # Ярон
    1145253479779151932: {"voice_exp": 400, "text_exp": 2000}, # Высшая каламитас
}

async def add_voice_time():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for guild in bot.guilds:
            for member in guild.members:
                if member.voice and member.voice.channel:
                    if member.id not in voice_time:
                        voice_time[member.id] = 0
                    voice_time[member.id] += 1
        await asyncio.sleep(60)

async def add_message_time():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for guild in bot.guilds:
            for channel in guild.text_channels:
                async for message in channel.history(limit=None):
                    if message.author.id not in message_time:
                        message_time[message.author.id] = 0
                    message_time[message.author.id] += 1
        await asyncio.sleep(60)

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rank(self, inter):
        voice_exp = voice_time.get(inter.author.id, 0)
        message_exp = message_time.get(inter.author.id, 0)
        total_exp = voice_exp + message_exp
        for role_id, exp_required in rank_roles.items():
            if total_exp >= exp_required["voice_exp"] or total_exp >= exp_required["text_exp"]:
                role = inter.guild.get_role(role_id)
                if role:
                    await inter.author.add_roles(role, reason="Повышение уровня")
                    await inter.reply(f"Ваш уровень повышен до роли {role.name}.", ephemeral=True)
                voice_time[inter.author.id] = 0
                message_time[inter.author.id] = 0
                break

    @commands.command()
    async def delete_all(self, inter):
        for role_id in rank_roles.keys():
            role = inter.guild.get_role(role_id)
            if role:
                await role.delete(reason="Удаление всех ранговых ролей")
        await inter.reply("Все ранговые роли успешно удалены.", ephemeral=True)

    @commands.command()
    async def give_roles(self, inter, member: disnake.Member, role: disnake.Role):
        await member.add_roles(role, reason="Выдана через команду /give_roles")
        await inter.reply(f"Роль {role.name} успешно выдана пользователю {member.display_name}.", ephemeral=True)

def setup(bot):
    bot.loop.create_task(add_voice_time())
    bot.loop.create_task(add_message_time())
    bot.add_cog(Ranking(bot))
import disnake
from disnake.ext import commands
from colorama import Fore, Style
import asyncio
import config

intents = disnake.Intents.default()
intents.typing = False
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

experience = {}

rank_roles = {
    "Слизень": 10,
    "Зомби": 50,
    "Глаз": 100
}

role_ids = {
    "Слизень": 1243948700280033362,
    "Зомби": 1243948698678067281,
    "Глаз": 1243948692965425222
}

async def voice_experience():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for guild in bot.guilds:
            for member in guild.members:
                if member.voice and member.voice.channel:
                    experience[member.id] = experience.get(member.id, 0) + 1
                    await check_rank(member)
        await asyncio.sleep(60)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    experience[message.author.id] = experience.get(message.author.id, 0) + 1
    await check_rank(message.author)
    await bot.process_commands(message)

async def check_rank(member):
    user_experience = experience.get(member.id, 0)
    for rank, exp_needed in rank_roles.items():
        if user_experience >= exp_needed:
            role_id = role_ids.get(rank)
            if role_id:
                role = member.guild.get_role(role_id)
                if role and role not in member.roles:
                    await member.add_roles(role)
                    await member.send(f"Поздравляю! Вы достигли ранга **{rank}**!")
            else:
                print(f"ID роли для {rank} не найден.")

@bot.command()
async def rank(ctx):
    user_experience = experience.get(ctx.author.id, 0)
    await ctx.send(f"{ctx.author.name}, ваш текущий опыт: {user_experience}")

@bot.event
async def on_ready():
    print(Fore.GREEN + """
███╗░░██╗██╗░░██╗░░░░░░██████╗░░█████╗░██╗░░░░░███████╗░██████╗
████╗░██║██║░██╔╝░░░░░░██╔══██╗██╔══██╗██║░░░░░██╔════╝██╔════╝
██╔██╗██║█████═╝░█████╗██████╔╝██║░░██║██║░░░░░█████╗░░╚█████╗░
██║╚████║██╔═██╗░╚════╝██╔══██╗██║░░██║██║░░░░░██╔══╝░░░╚═══██╗
██║░╚███║██║░╚██╗░░░░░░██║░░██║╚█████╔╝███████╗███████╗██████╔╝
╚═╝░░╚══╝╚═╝░░╚═╝░░░░░░╚═╝░░╚═╝░╚════╝░╚══════╝╚══════╝╚═════╝░

""" + Style.RESET_ALL)
    print("Бот приветствует вас и готов к работе!")
    await bot.change_presence(status=disnake.Status.idle)

    for guild in bot.guilds:
        for member in guild.members:
            await check_rank(member)

bot.loop.create_task(voice_experience())

bot.load_extension("cogs.ranking")

bot.run('TOKEN')
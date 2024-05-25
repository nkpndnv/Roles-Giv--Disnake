import disnake
from disnake.ext import commands
from colorama import Fore, Style
import asyncio

intents = disnake.Intents.default()
intents.typing = False
intents.message_content = True

bot = commands.InteractionBot(intents=disnake.Intents.all())


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

def setup(bot):
    bot.add_cog(Ranking(bot))

bot.run('TOKEN')
import discord
from discord.ext import commands
from config import TOKEN
from module_loader import load_modules

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

load_modules(bot)

bot.run(TOKEN)

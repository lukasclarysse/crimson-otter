import discord
from discord.ext import commands
from config import TOKEN
from commands import register_commands
from events import register_events

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

register_commands(bot)
register_events(bot)

bot.run(TOKEN)

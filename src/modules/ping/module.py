from discord.ext import commands

def setup(bot: commands.Bot):
    @bot.command()
    async def ping(ctx):
        latency = round(bot.latency * 1000)
        await ctx.send(f"pong`{latency}ms`")
from discord.ext import commands
import discord

from config import LOG_CHANNEL
from embeds import SUPREME_LEADER_INCIDENT_EMBED
from logging_setup import log


def register_commands(bot):
    @bot.command()
    async def ping(ctx):
        latency = round(bot.latency * 1000)
        await ctx.send(f"pong `{latency}ms`")

    @bot.command()
    async def bully(ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("nobody likes you")
            return

        if member.id == bot.user.id:
            await ctx.send(
                "The Supreme leader has reviewed your insolence. "
                "Your complaint has been rejected."
            )

            mod_channel = bot.get_channel(LOG_CHANNEL)

            if mod_channel:
                try:
                    embed = SUPREME_LEADER_INCIDENT_EMBED.copy()
                    embed.description = (
                        f"User: {ctx.author.mention}\n"
                        f"Attempted to bully: {bot.user.mention}"
                    )
                    embed.timestamp = ctx.message.created_at

                    embed.add_field(
                        name="Command",
                        value=ctx.message.content,
                        inline=False
                    )

                    embed.set_footer(
                        text=f"User ID: {ctx.author.id}"
                    )

                    await mod_channel.send(embed=embed)

                except discord.HTTPException as e:
                    log.error(
                        f"Failed to log Supreme Leader incident: {e}"
                    )

            try:
                await ctx.author.kick(
                    reason="Attempted to bully the Supreme Bot"
                )

                log.info(
                    f"Kicked {ctx.author} for attempting to bully the bot"
                )

            except discord.Forbidden as e:
                log.error(
                    f"Discord refused to kick {ctx.author} "
                    f"(ID: {ctx.author.id}): {e}"
                )

            except discord.HTTPException as e:
                log.error(
                    f"Discord API error while kicking {ctx.author}: {e}"
                )

            return

        await ctx.send(f"nobody likes {member.display_name}")

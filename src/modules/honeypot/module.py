
import discord
from discord.ext import commands

from config import (
    BOT_ACTION,
    HONEYPOT_CHANNEL,
    LOG_CHANNEL,
    PURGE_TIMEFRAME,
)
from logging_setup import log

from .embeds import (
    HONEYPOT_WARNING_EMBED,
    HONEYPOT_WARNING_MARKER,
)
from .moderation import delete_recent_user_messages
from .kick_counter import get_kick_count, increment_kick_count


async def ensure_honeypot_warning(bot):
    channel = bot.get_channel(HONEYPOT_CHANNEL)

    if not channel:
        log.warning("Honeypot channel not found")
        return

    kick_count = await get_kick_count()

    embed = HONEYPOT_WARNING_EMBED.copy()
    embed.add_field(
        name="Total kicks",
        value=f"**{kick_count:,}**",
        inline=False,
    )

    async for msg in channel.history(limit=50):
        for emb in msg.embeds:
            if (
                emb.footer
                and HONEYPOT_WARNING_MARKER
                in (emb.footer.text or "")
            ):
                try:
                    await msg.edit(embed=embed)
                    log.info("Honeypot warning updated")
                except discord.HTTPException as e:
                    log.error(f"Failed to update warning: {e}")
                return

    try:
        await channel.send(embed=embed)
        log.info("Honeypot warning posted")
    except discord.HTTPException as e:
        log.error(f"Failed to send warning: {e}")


def register_events(bot):

    @bot.event
    async def on_ready():
        log.info(f"Bot online as {bot.user}")
        await ensure_honeypot_warning(bot)

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        await bot.process_commands(message)

        if message.channel.id != HONEYPOT_CHANNEL:
            return

        if message.guild is None:
            return

        log.info(
            f"HONEYPOT TRIGGER: {message.author} "
            f"in #{message.channel.name}"
        )

        guild = message.guild
        mod_channel = bot.get_channel(LOG_CHANNEL)

        if mod_channel:
            try:
                embed = discord.Embed(
                    title="Honeypot Alert",
                    description=f"User: {message.author.mention}",
                    color=discord.Color.red(),
                    timestamp=message.created_at,
                )

                embed.add_field(
                    name="Message",
                    value=message.content or "*No content*",
                    inline=False,
                )

                embed.set_footer(
                    text=f"User ID: {message.author.id}"
                )

                await mod_channel.send(embed=embed)

            except discord.HTTPException as e:
                log.error(f"Failed to send log embed: {e}")

        try:
            await message.delete()
        except discord.HTTPException as e:
            log.warning(f"Failed to delete honeypot message: {e}")

        try:
            deleted = await delete_recent_user_messages(
                guild,
                message.author,
                PURGE_TIMEFRAME,
            )

            if mod_channel and deleted > 0:
                await mod_channel.send(
                    f"Deleted `{deleted}` recent messages from "
                    f"{message.author.mention} "
                    f"(last `{PURGE_TIMEFRAME}` seconds)."
                )

        except Exception as e:
            log.error(f"Failed to purge messages: {e}")

        try:
            member = await guild.fetch_member(message.author.id)

        except discord.NotFound:
            log.warning(
                f"Could not find member {message.author} "
                "for moderation action"
            )
            return

        except discord.HTTPException as e:
            log.error(f"Failed to fetch member: {e}")
            return

        try:
            if BOT_ACTION == "ban":
                await guild.ban(
                    member,
                    reason="Triggered honeypot",
                )

                log.info(f"Banned {member}")

            elif BOT_ACTION == "kick":
                await member.kick(
                    reason="Triggered honeypot",
                )

                log.info(f"Kicked {member}")

                await increment_kick_count()

                await ensure_honeypot_warning(bot)

            else:
                log.warning(
                    f"Unsupported BOT_ACTION: {BOT_ACTION}"
                )

        except discord.Forbidden:
            log.error(
                f"Missing permissions to {BOT_ACTION} {member}"
            )

        except discord.HTTPException as e:
            log.error(
                f"Discord API error while executing "
                f"{BOT_ACTION} on {member}: {e}"
            )


def setup(bot: commands.Bot):
    register_events(bot)

import discord

from config import BOT_ACTION


HONEYPOT_WARNING_MARKER = "HONEYPOT_WARNING_V3"
ACTION_TEXT = BOT_ACTION.capitalize()


HONEYPOT_WARNING_EMBED = discord.Embed(
    title="DO NOT POST HERE",
    description=(
        "**This is a honeypot channel.**\n\n"
        f"Posting anything here will result in an automatic **{ACTION_TEXT}**."
    ),
    color=discord.Color.red(),
)

HONEYPOT_WARNING_EMBED.set_footer(
    text=HONEYPOT_WARNING_MARKER
)
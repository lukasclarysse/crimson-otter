import asyncio
import random

import discord
from discord.ext import commands

from data import (
    CONSULTATION_EVENTS,
    LEAGUE_EVENTS,
    FAILURE_MESSAGES,
    ORACLE_RESPONSES,
)


def make_progress_bar(progress, length=20):
    filled = round((progress / 100) * length)
    empty = length - filled

    return f"[{'█' * filled}{'░' * empty}] {progress}%"


def build_message(question, progress, event):
    return (
        "**ORACLE CONSULTATION**\n\n"
        f"> {question}\n\n"
        f"{make_progress_bar(progress)}\n\n"
        f"*{event}*"
    )


def register_oracle(bot):
    @bot.command()
    async def oracle(ctx, *, question=None):
        if not question:
            await ctx.send(
                "The Oracle requires a question.\n"
                "Try `$oracle should I play ranked?`"
            )
            return

        progress = 0

        message = await ctx.send(
            build_message(
                question,
                progress,
                "Awakening the Oracle..."
            )
        )

        while True:
            await asyncio.sleep(random.uniform(0.4, 0.8))

            if random.randint(1, 100) == 1:
                failure = random.choice(FAILURE_MESSAGES)

                await message.edit(
                    content=(
                        "**ORACLE CONSULTATION FAILED**\n\n"
                        f"> {question}\n\n"
                        f"{make_progress_bar(progress)}\n\n"
                        f"**{failure}**"
                    )
                )

                return

            roll = random.randint(1, 100)

            if roll <= 60:
                progress += random.randint(4, 10)

            elif roll <= 82:
                progress -= random.randint(1, 6)

            elif roll <= 92:
                progress -= random.randint(8, 18)

            elif roll == 93:
                progress = 0

            else:
                pass

            progress = max(0, min(progress, 100))

            if random.randint(1, 100) <= 40:
                event = random.choice(LEAGUE_EVENTS)
            else:
                event = random.choice(CONSULTATION_EVENTS)

            if random.randint(1, 100) <= 5:
                event = "The Oracle has reviewed your match history."

            if random.randint(1, 100) <= 3:
                event = "The Oracle has consulted a Silver IV Yasuo main."

            if random.randint(1, 100) <= 2:
                event = "The Oracle has made a terrible mistake."

            await message.edit(
                content=build_message(
                    question,
                    progress,
                    event
                )
            )

            # Success.
            if progress >= 100:
                await asyncio.sleep(random.uniform(0.5, 1.2))

                response = random.choice(ORACLE_RESPONSES)

                await message.edit(
                    content=(
                        "**ORACLE CONSULTATION COMPLETE**\n\n"
                        f"> {question}\n\n"
                        f"{make_progress_bar(100)}\n\n"
                        "**THE ORACLE HAS SPOKEN.**\n\n"
                        f"*{response}*"
                    )
                )

                return

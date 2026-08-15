import discord
from discord.ext import commands
import asyncio

class React(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        for owner in self.bot.owner_ids:
            if f"<@{owner}>" in message.content:
                try:
                    # This used to give one specific Discord ID (the original
                    # developer's) an extra 4th emoji that no one else got.
                    # Now every configured owner gets the same reaction set.
                    emojis = [
                        "<a:BlackCrown:1448949787842973697>",
                        "<a:Active_Developer:1448949755181793280>",
                        "<a:Staff:1538167256096178216>"
                    ]

                    for emoji in emojis:
                        try:
                            await message.add_reaction(emoji)
                        except discord.HTTPException:
                            pass  # ignore if emoji is invalid or not accessible

                except discord.errors.RateLimited as e:
                    await asyncio.sleep(e.retry_after)
                except Exception as e:
                    print(f"An unexpected error occurred Auto react owner mention: {e}")
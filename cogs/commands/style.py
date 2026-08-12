import discord
from discord.ext import commands
from core.Cog import Cog
from utils.style_engine import ProfileStyleService

class Style(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setstyle")
    @commands.has_permissions(manage_nicknames=True)
    async def set_style(self, ctx, font_id: int, effect_id: int, color_decimal: int):
        """
        Change the bot's profile name style directly.
        Usage: !setstyle <font_id> <effect_id> <color_decimal>
        """
        await ctx.send("🔄 Processing custom style adjustment, please wait...")

        # Basic input validation based on the service architecture
        if font_id < 1 or font_id > 12:
            return await ctx.send("❌ Invalid Font ID! Choose a number between 1 and 12.")
        
        if effect_id < 1 or effect_id > 6:
            return await ctx.send("❌ Invalid Effect ID! Choose a number between 1 and 6.")

        # Structure the style dictionary format dynamically
        custom_style = {
            "font_id": font_id,
            "effect_id": effect_id,
            "colors": [color_decimal]
        }

        try:
            # Call the engine instance to trigger the API patching mechanism
            service = ProfileStyleService(self.bot)
            success = await service.apply_style(str(ctx.guild.id), self.bot.user.name, custom_style)
            
            if success:
                embed = discord.Embed(
                    title="✅ Style Updated Successfully",
                    description=f"Direct changes applied to **{self.bot.user.name}** profile configurations.",
                    color=discord.Color.green()
                )
                embed.add_field(name="Font ID", value=str(font_id), inline=True)
                embed.add_field(name="Effect ID", value=str(effect_id), inline=True)
                embed.add_field(name="Color (Decimal)", value=str(color_decimal), inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Failed to update profile layout. Verify API permissions or wait out rate-limits.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred during runtime execution: {e}")

async def setup(bot):
    await bot.add_cog(Style(bot))
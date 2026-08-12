import discord
from discord.ext import commands
from discord import app_commands, Interaction
from difflib import get_close_matches
from contextlib import suppress
from core import Context
from core.zyrox import zyrox
from core.Cog import Cog
from utils.Tools import getConfig
from itertools import chain
import json
from utils import help as vhelp
from utils import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
import asyncio
from utils.config import serverLink
from utils.Tools import *

color = 0xFF0000
client = zyrox()

class HelpCommand(commands.HelpCommand):

  async def send_ignore_message(self, ctx, ignore_type: str):
    if ignore_type == "channel":
      await ctx.reply(f"This channel is ignored.", mention_author=False)
    elif ignore_type == "command":
      await ctx.reply(f"{ctx.author.mention} This Command, Channel, or You have been ignored here.", delete_after=6)
    elif ignore_type == "user":
      await ctx.reply(f"You are ignored.", mention_author=False)

  async def on_help_command_error(self, ctx, error):
    errors = [
      commands.CommandOnCooldown, commands.CommandNotFound,
      discord.HTTPException, commands.CommandInvokeError
    ]
    if not type(error) in errors:
      await self.context.reply(f"Unknown Error Occurred\n{error.original}",
                               mention_author=False)
    else:
      if type(error) == commands.CommandOnCooldown:
        return
    return await super().on_help_command_error(ctx, error)

  async def command_not_found(self, string: str) -> None:
    ctx = self.context
    check_ignore = await ignore_check().predicate(ctx)
    check_blacklist = await blacklist_check().predicate(ctx)

    if not check_blacklist:
        return

    if not check_ignore:
        await self.send_ignore_message(ctx, "command")
        return

    cmds = (str(cmd) for cmd in self.context.bot.walk_commands())
    matches = get_close_matches(string, cmds)

    embed = discord.Embed(
        title="striker Helper",
        description=f">>> **Ops! Command not found with the name** `{string}`.",
        color=0xFF0000
    )
                          
    #if matches:
        #match_list = "\n".join([f"{index}. `{match}`" for index, match in enumerate(matches, start=1)])
        #embed.add_field(name="Did you mean:", value=match_list, inline=True)

    await ctx.reply(embed=embed, mention_author=True)

  async def send_bot_help(self, mapping):
    ctx = self.context
    check_ignore = await ignore_check().predicate(ctx)
    check_blacklist = await blacklist_check().predicate(ctx)

    if not check_blacklist:
      return

    if not check_ignore:
      await self.send_ignore_message(ctx, "command")
      return

    # Show loading embed
    loading_embed = discord.Embed(
      description="<a:loading:1536975745681727538> Loading help Menu...",
      color=0xFF0000
    )
    loading_msg = await ctx.reply(embed=loading_embed)

    # Wait 2 seconds
    await asyncio.sleep(2)

    # Delete loading message
    with suppress(discord.NotFound):
      await loading_msg.delete()

    data = await getConfig(self.context.guild.id)
    prefix = data["prefix"]
    filtered = await self.filter_commands(self.context.bot.walk_commands(), sort=True)

    embed = discord.Embed(
        description=(
         f"**<a:arrowBlurple:1536977717206061106> __Checkout What i can do__**\n"        
         f"**<a:arrow:1536977958659432520> Type {prefix}antinuke enable**\n"
         f"**<a:arrow:1536977958659432520> Server Prefix:** `{prefix}`\n"
         f"**<a:arrow:1536977958659432520> Total Commands:** `{len(set(self.context.bot.walk_commands()))}`\n"),         
        color=0xFF0000)
    embed.set_author(name=f"{ctx.author}", 
                     icon_url=ctx.author.display_avatar.url)
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    
    embed.add_field(
        name="☁️ __**Main Features**__",
        value=">>> \n 🔐 `»` Security\n" 
              " <:bots:1536976337787686912> `»` Automoderation\n"
              " <:utility:1535979646930255924> `»` Utility\n" 
              " <a:DJ_MUSIC:1535979683949060208> `»` Music\n"
              " <:react:1535981565920936046> `»` Autoreact & responder\n"
              " <:moderation:1535981718543016006> `»` Moderation\n"
              " <a:rockandrole:1535985141107662959> `»` Autorole & Invc\n"
              " <a:AI_verify_certified_owo_lol_anim:1535983008698601582> `»` Fun\n"
              " <a:other_games:1535983231017685042> `»` Games\n" 
              " <a:No_:1535983407241109544> `»` Ignore Channels\n"
              " <:wifi:1535983550732701806> `»` Server\n"
              " <:Unmute:1535983705947115571> `»` Voice\n"
              " <a:welcome_swift:1535984044263735406> `»` Welcomer\n"  
              " <a:float_gift:1535984187431976981> `»` Giveaway\n"
              " <a:ticket:1535984605755351100> `»` Ticket <:New:1448949337395695616>\n"
              " <:Inviterbadge:1535982678472392705> `»` Invite Tracker <:New:1448949337395695616>\n"
    )
    
    embed.add_field(
        name=" <a:mod:1536978396062425119> __**Extra Features**__",
        value=">>> \n <a:Books_:1536977542815416339> `»` Advance Logging\n"
              " <a:star_red:1535985476534669413> `»` Vanityroles\n"
              
              " <a:six_sevennn:1536978639453822996> `»` Counting <:New:1448949337395695616>\n"
              " <a:arrow_arrow:1536979214803275796> `»` J2C <:New:1448949337395695616>\n"
              " <a:wrobot_swift:1536979951624912938> `»` AI <:New:1448949337395695616>\n"
              " <a:Nitro_Boost:1535986050189623380> `»` Boost <:New:1448949337395695616>\n"
              " <a:levelup:1535986508429787236> `»` Leveling <:New:1448949337395695616>\n"
              " <a:pw_pin:1535986399159914600> `»` Sticky <:New:1448949337395695616>\n"
              " <a:Verified:1535986177264324628> `»` Verification <:New:1448949337395695616>\n"
              " <a:lock_key:1535986624788439041> `»` Encryption <:New:1448949337395695616>\n" 
              " <a:MINECRAFT:1535986721521664051> `»` Minecraft <:New:1448949337395695616>\n"
              " <:Messages:1535986825750126674> `»` Joindm <:New:1448949337395695616>\n"
              " 🎂 `»` Birthday <:New:1448949337395695616>\n"
              " <:role:1535987179761696812> `»` Customrole\n"           
    )

    embed.set_footer(
      text=f"Requested By {self.context.author} | [Support](https://discord.gg/jj87n6fDQX)",
    )
    
    view = vhelp.View(mapping=mapping, ctx=self.context, homeembed=embed, ui=2)
    await ctx.reply(embed=embed, view=view)

  async def send_command_help(self, command):
    ctx = self.context
    check_ignore = await ignore_check().predicate(ctx)
    check_blacklist = await blacklist_check().predicate(ctx)

    if not check_blacklist:
      return

    if not check_ignore:
      await self.send_ignore_message(ctx, "command")
      return

    zyrox = f">>> {command.help}" if command.help else '>>> No Help Provided...'
    embed = discord.Embed(
        description=f"""{zyrox}""",
        color=color)
    alias = ' & '.join(command.aliases)

    embed.add_field(name="**Alt cmd**",
                      value=f"```{alias}```" if command.aliases else "No Alt cmd",
                      inline=False)
    embed.add_field(name="**Usage**",
                      value=f"```{self.context.prefix}{command.signature}```\n")
    embed.set_author(name=f"{command.qualified_name.title()} Command")
    embed.set_footer(text="<[] = optional | < > = required • Use Prefix Before Commands.")
    await self.context.reply(embed=embed, mention_author=False)

  def get_command_signature(self, command: commands.Command) -> str:
    parent = command.full_parent_name
    if len(command.aliases) > 0:
      aliases = ' | '.join(command.aliases)
      fmt = f'[{command.name} | {aliases}]'
      if parent:
        fmt = f'{parent}'
      alias = f'[{command.name} | {aliases}]'
    else:
      alias = command.name if not parent else f'{parent} {command.name}'
    return f'{alias} {command.signature}'

  def common_command_formatting(self, embed_like, command):
    embed_like.title = self.get_command_signature(command)
    if command.description:
      embed_like.description = f'{command.description}\n\n{command.help}'
    else:
      embed_like.description = command.help or 'No help found...'

  async def send_group_help(self, group):
    ctx = self.context
    check_ignore = await ignore_check().predicate(ctx)
    check_blacklist = await blacklist_check().predicate(ctx)

    if not check_blacklist:
      return

    if not check_ignore:
      await self.send_ignore_message(ctx, "command")
      return

    entries = [
        (
            f"`{self.context.prefix}{cmd.qualified_name}`\n",
            f"{cmd.short_doc if cmd.short_doc else ''}\n\u200b"
        )
        for cmd in group.commands
      ]

    count = len(group.commands)

    embeds = FieldPagePaginator(
      entries=entries,
      title=f"{group.qualified_name.title()} [{count}]",
      description="< > Duty | [ ] Optional\n",
      per_page=4
    ).get_pages()   
    
    paginator = Paginator(ctx, embeds)
    await paginator.paginate()

  async def send_cog_help(self, cog):
    ctx = self.context
    check_ignore = await ignore_check().predicate(ctx)
    check_blacklist = await blacklist_check().predicate(ctx)

    if not check_blacklist:
      return

    if not check_ignore:
      await self.send_ignore_message(ctx, "command")
      return

    entries = [(
      f"> `{self.context.prefix}{cmd.qualified_name}`",
      f"-# Description : {cmd.short_doc if cmd.short_doc else ''}"
      f"\n\u200b",
    ) for cmd in cog.get_commands()]
    paginator = Paginator(source=FieldPagePaginator(
      entries=entries,
      title=f"NEON~V2's {cog.qualified_name.title()} ({len(cog.get_commands())})",
      description="`<..> Required | [..] Optional`\n\n",
      color=0xFF0000,
      per_page=4),
                          ctx=self.context)
    await paginator.paginate()


class Help(Cog, name="help"):

  def __init__(self, client: zyrox):
    self._original_help_command = client.help_command
    attributes = {
      'name': "help",
      'aliases': ['h'],
      'cooldown': commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user),
      'help': 'Shows help about bot, a command, or a category'
    }
    client.help_command = HelpCommand(command_attrs=attributes)
    client.help_command.cog = self

  async def cog_unload(self):
    self.help_command = self._original_help_command
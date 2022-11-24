import asyncio
import datetime
import logging

import discord
from discord.ext import commands, tasks

from utils.secret import mods_role
# from utils.logs import CommandLog


logger = logging.getLogger(__name__)


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log
        self.autoclean_spoil_chan.start()  # pylint: disable=no-member

    @commands.command()
    @commands.has_any_role(*mods_role)
    async def kick(self, ctx):
        """Kick user."""
        member_list = ctx.message.mentions
        for member in member_list:
            await member.kick()
        today = datetime.date.today().strftime("%d/%m/%Y")
        time = datetime.datetime.now().strftime("%Hh%Mm%Ss")
        self.log.log_write(today, time,
                           ctx.channel.name.lower(),
                           ctx.command.name.lower(),
                           ctx.author.name.lower())
        await ctx.send(content="Adios muchachos !")

    @kick.error
    async def kick_error(self, ctx, error):
        """Handle error in !kick command (MissingAnyRole)."""
        await ctx.send(content=f"Tu n'as pas de pouvoirs{ctx.author.mention} !")  # noqa: E501

    @commands.command()
    @commands.has_any_role(*mods_role)
    async def ban(self, ctx):
        """Ban user."""
        member_list = ctx.message.mentions
        for member in member_list:
            await member.ban(delete_message_days=3)
        today = datetime.date.today().strftime("%d/%m/%Y")
        time = datetime.datetime.now().strftime("%Hh%Mm%Ss")
        self.log.log_write(today, time,
                           ctx.channel.name.lower(),
                           ctx.command.name.lower(),
                           ctx.author.name.lower())

    @ban.error
    async def ban_error(self, ctx, error):
        """Handle error in !ban command (MissingAnyRole)."""
        await ctx.send(content=f"Tu n'as pas de pouvoirs{ctx.author.mention} !")  # noqa: E501

    @commands.command()
    @commands.has_any_role(*mods_role)
    async def nomorespoil(self, ctx):
        """Spam dots to clear potential spoils."""
        await ctx.send("\n".join(["..." for i in range(50)]))

    @commands.Cog.listener()
    async def on_command(self, ctx):
        # If test if not very fancy
        # (no @decorator of special event on_cog_command for this ??)
        # But otherwise, on_command() triggers on ALL commands (including other cogs)  # noqa: E501
        # So we test if we're in current cog (self)
        if ctx.command.cog_name == self.qualified_name:
            logger.info(f"Command {str(ctx.command):15} invoked by {str(ctx.author):15} in room {str(ctx.channel):15} with message {ctx.message.content}")  # noqa: E501

    @tasks.loop(hours=24)
    async def autoclean_spoil_chan(self):
        if spoil_chan := discord.utils.get(self.bot.guild.text_channels, name='spoil'):
            last_message = await spoil_chan.fetch_message(spoil_chan.last_message_id)
            last_text = last_message.content
            # Test on the last message text in spoil channel
            if last_text.endswith("...\n...\n..."):
                logger.info("#spoil channel is allready clean, passing.")
                pass
            else:
                # Send lines of "..." to get rid of spoilers
                await spoil_chan.send("\n".join(["..." for i in range(50)]))
                logger.info("#spoil channel has been cleaned.")
        else:
            logger.error("No spoil channel")

    @autoclean_spoil_chan.before_loop
    async def before_autoclean_spoil_chan(self):
        """Intiliaze autoclean_spoil_chan loop."""
        await self.bot.wait_until_ready()
        await asyncio.sleep(14400)  # Wait 4 houres, to fire at 4AM

import datetime

import discord
from discord.ext import commands

from utils.secret import mods_role
from utils.logs import CommandLog

class Mod(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.log = bot.log
    

    @commands.command()
    @commands.has_any_role(*mods_role)
    async def kick(self,ctx):
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
    async def kick_error(self,ctx, error):
        """Handle error in !kick command (MissingAnyRole)."""
        await ctx.send(content=f"Tu n'as pas de pouvoirs{ctx.author.mention} !")  # noqa: E501


    @commands.command()
    @commands.has_any_role(*mods_role)
    async def ban(self,ctx):
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
    async def ban_error(self,ctx, error):
        """Handle error in !ban command (MissingAnyRole)."""
        await ctx.send(content=f"Tu n'as pas de pouvoirs{ctx.author.mention} !")  # noqa: E501

    @commands.command()
    @commands.has_any_role(*mods_role)
    async def nomorespoil(self,ctx):
        """Spam dots to clear potential spoils."""
        await ctx.send("\n".join(["..." for i in range(50)]))
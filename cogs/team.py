import datetime

import discord
from discord.ext import commands

from utils.logs import CommandLog
from utils.secret import staff_role


class Team(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._role_dcteam = bot.role_dcteam
        self.log = bot.log

    
    @commands.command()
    @commands.has_any_role(*staff_role)
    async def team(self,ctx):
        """Give 'team' role to user list."""
        member_list = ctx.message.mentions  # une liste d'objets
        counter = 0
        if not member_list:
            pass
        else:
            for member in member_list:
                if self._role_dcteam in member.roles:  # le counter c'est pour voir si tous les membres mentionnés  # noqa: E501
                    counter += 1
                await member.add_roles(self._role_dcteam)  # sont dans la team, alors on n'affiche pas le message de bienvenue  # noqa: E501
            if counter == len(member_list):
                return None
            await ctx.send(content="Bienvenue dans la Team !")


    @team.error
    async def team_error(self,ctx, error):
        """Handle error in command !team (MissingAnyRole)."""
        await ctx.send(content="Bien tenté mais tu n'as pas de pouvoir ici !")

    @commands.command()
    @commands.has_any_role(*staff_role)
    async def clear(self,ctx, number):
        """Clear n messages."""
        nbr_msg = int(number)
        messages = await ctx.channel.history(limit=nbr_msg + 1).flatten()
        await ctx.channel.delete_messages(messages)
        await ctx.send(content=f"J'ai supprimé {nbr_msg} messages", delete_after=5)
        today = datetime.date.today().strftime("%d/%m/%Y")
        time = datetime.datetime.now().strftime("%Hh%Mm%Ss")
        self.log.log_write(today, time,
                    ctx.channel.name.lower(),
                    ctx.command.name.lower(),
                    ctx.author.name.lower())


    @clear.error
    async def clear_error(self,ctx, error):
        """Handle error in !clear command (MissingAnyRole)."""
        await ctx.send(content=f"Tu n'as pas le pouvoir{ctx.author.mention} !")
import datetime

# import discord
from discord.ext import commands

# from utils.logs import CommandLog
from utils.secret import staff_role


class Team(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._role_dcteam = bot.role_dcteam
        self.log = bot.log

    @commands.command()
    @commands.has_any_role(*staff_role)
    async def team(self, ctx: commands.Context):
        """Give 'team' role to user list."""
        if member_list := ctx.message.mentions:
            for member in member_list:
                if self._role_dcteam not in member.roles:
                    await member.add_roles(self._role_dcteam)
                    await ctx.send(content="Bienvenue dans la Team !")

    @team.error
    async def team_error(self, ctx, error):
        """Handle error in command !team (MissingAnyRole)."""
        await ctx.send(content="Bien tenté mais tu n'as pas de pouvoir ici !")

    @commands.command(aliases=['clean'])
    @commands.has_any_role(*staff_role)
    async def clear(self, ctx, nbr_msg: int):
        """Clear n messages."""
        messages = [message async for message in ctx.channel.history(limit=nbr_msg + 1)]
        await ctx.channel.delete_messages(messages)
        await ctx.send(content=f"J'ai supprimé {nbr_msg} messages", delete_after=2)
        today = datetime.date.today().strftime("%d/%m/%Y")
        time = datetime.datetime.now().strftime("%Hh%Mm%Ss")
        self.log.log_write(today, time,
                           ctx.channel.name.lower(),
                           ctx.command.name.lower(),
                           ctx.author.name.lower())

    @clear.error
    async def clear_error(self, ctx, error):
        """Handle error in !clear command (MissingAnyRole)."""
        await ctx.send(content=f"Tu n'as pas le pouvoir{ctx.author.mention} !")

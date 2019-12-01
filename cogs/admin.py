import datetime
import os
import random
import sys



import discord
from discord.ext import commands

from utils.logs import CommandLog
from utils.tools import args_separator_for_log_function
from utils.secret import admin_role

class Admin(commands.Cog):
    def __init__ (self,bot):
        self.bot = bot
        self.giflist = bot.gifs
        self.log = bot.log


    @commands.command()
    @commands.is_owner()
    async def admin(self,ctx):
        """Help for admin user."""
        embed = discord.Embed(color=0x0000FF)
        embed.add_field(name="gifadd",
                        value="!gifadd <name> <url> <bool> (bool : public(True) or private(False) )",  # noqa: E501
                        inline=False)
        embed.add_field(name="gifdelete", value="!gifdelete <name>", inline=False)
        embed.add_field(name="log_latest", value="!log_latest <int>", inline=False)
        embed.add_field(name="logs", value="!logs <date> <user> <command> <channel>\n args are optional for filtering, for today, say <date> = today. Otherwise date=dd/mm/yyyy", inline=False)  # noqa:E501
        embed.add_field(name="sleep", value="make the bot sleep for <numb> seconds\n  Syntax : !sleep <number>", inline=False)
        embed.add_field(name="kill", value="Kill the bot.", inline=False)
        await ctx.author.send(embed=embed)


    @commands.command()
    @commands.is_owner()
    async def gifadd(self,ctx, name, url, bool):
        """Add gif in gif dictionary and gif json file."""
        name = name.lower()

        bool = bool.lower()
        self.giflist.gif_add(name, url, bool)
        await ctx.send(content=f"gif {name} ajouté !", delete_after=2)


    @commands.command()
    @commands.is_owner()
    async def gifdelete(self,ctx, name):
        """Delete gif in gif dictionary and gif json file."""
        name = name.lower()
        self.giflist.gif_delete(name)
        await ctx.send(content=f"gif {name} supprimé !", delete_after=2)

    @commands.command()
    @commands.has_any_role(*admin_role)
    async def restart(self,ctx):
        """Restart bot."""
        await ctx.send('Restarting.')
        os.execv(__file__, sys.argv)


    @restart.error
    async def restart_error(self,ctx, error):
        """Handle error in !restart command (MissingAnyRole)."""
        await ctx.send('Nope.')

    @commands.command()
    @commands.is_owner()
    async def logs(self,ctx, date="today", *args):
        """Send some logs in private message about moderation commands usage.

        Args:
            date (str): today(default) or date as DD/MM/YYYY
            args: up to 3 elements, speifying command, user, channel

        Examples:
            log today homer general: list homer commands in #general channel
            log 05/06/2019 faq: list all moderaiton commands in #faq on 05/06/2019

        """
        embed = discord.Embed(title="logs", colour=0xe7191f)

        # arg_lists is always ["user", "command", "channel"]
        args_list = args_separator_for_log_function(self.bot.guild, args)

        if date == "today":
            date = datetime.date.today().strftime("%d/%m/%Y")

        bin_array = [int(i is not None) for i in args_list]  # convert ["foo", None, None] to [1, 0, 0]  # noqa:E501
        n = int("".join(str(x) for x in bin_array), 2)  # binary array to int

        user, command, channel = args_list

        if self.log.log_read(date, *args_list) is not None:  # if it is None, there are no logs on the given date  # noqa:E501

            # we get a list of tuple in this format [(time,user,command,channel)]
            list_log = self.log.log_read(date, *args_list)  # to avoid multiple calling

            # if entries are not specified, then they are None
            if n == 0:  # [None, None, None]
                for v in list_log:
                    embed.add_field(name=v[0], value=f"{v[1]} used {v[2]} in {v[3]}", inline=False)  # nice embed  # noqa:E501

            elif n == 1:  # [None, None, channel]
                embed.set_footer(text=channel)
                for v in list_log:
                    embed.add_field(name=v[0], value=f"{v[1]} used {v[2]}", inline=False)  # noqa:E501

            elif n == 2:  # [None, command, None]
                embed.set_footer(text=f"users of {command}")
                for v in list_log:
                    embed.add_field(name=v[0], value=f"{v[1]} in {v[2]}", inline=False)  # noqa:E501

            elif n == 3:  # [None, command, channel]
                embed.set_footer(text=f"users of {command} in {channel}")
                for v in list_log:
                    embed.add_field(name=v[0], value=f"{v[1]}", inline=False)

            elif n == 4:  # [user, None, None]
                embed.set_footer(text=user)
                for v in list_log:
                    embed.add_field(name=v[0], value=f"used {v[1]} in {v[2]}", inline=False)  # noqa:E501

            elif n == 5:  # [user, None, channel]
                embed.set_footer(text=f"{user} commands in {channel}")
                for v in list_log:
                    embed.add_field(name=v[0], value=f"used {v[2]}", inline=False)

            elif n == 6:  # [user, command, None]
                embed.set_footer(text=f"{user} used {command}")
                for v in list_log:
                    embed.add_field(name=v[0], value=f"used in {v[2]}", inline=False)  # noqa:E501

            else:  # [user, command, channel]
                embed.set_footer(text=f"{user} used {command} in {channel}")
                for v in list_log:
                    embed.add_field(name=v[0], value=f"{v[1]}", inline=False)

            await ctx.author.send(embed=embed)
        else:  # no logs in the given date
            await ctx.author.send(content="Rien dans cette date !")


    @commands.command()
    @commands.is_owner()
    async def log_latest(self,ctx, numb=10):
        """Send latest logs."""
        embed = discord.Embed(title="latest logs")
        latest = self.log.log_latest(int(numb))
        for i in latest:
            embed.add_field(name='\u200B', value=i, inline=False)
        await ctx.author.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def kill(self,ctx):
        """Kill the bot."""
        await self.bot.logout()
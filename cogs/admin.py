import datetime
import os
import sys

import discord
from discord.ext import commands

# from utils.logs import CommandLog
from utils.tools import args_separator_for_log_function
from utils.secret import admin_role


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giflist = bot.gifs
        self.log = bot.log

    @commands.command()
    @commands.is_owner()
    async def admin(self, ctx):
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
    async def gifadd(self, ctx, name, url, scope: bool):
        """Add gif in gif dictionary and gif json file."""
        name = name.lower()

        self.giflist.gif_add(name, url, scope)
        await ctx.send(content=f"gif {name} ajouté !", delete_after=2)

    @commands.command()
    @commands.is_owner()
    async def gifdelete(self, ctx, name):
        """Delete gif in gif dictionary and gif json file."""
        name = name.lower()
        self.giflist.gif_delete(name)
        await ctx.send(content=f"gif {name} supprimé !", delete_after=2)

    @commands.command()
    @commands.has_any_role(*admin_role)
    async def restart(self, ctx):
        """Restart bot."""
        await ctx.send('Restarting.')
        # os.execv(__file__, sys.argv)  # old code (before cog)
        os.execv(sys.executable, [sys.executable] + sys.argv)

    @restart.error
    async def restart_error(self, ctx, error):
        """Handle error in !restart command (MissingAnyRole)."""
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send('Nope.')
        else:
            raise error

    @commands.command()
    @commands.is_owner()
    async def logs(self, ctx, date="today", *args):
        """Send some logs in private message about moderation commands usage.

        Args:
            date (str): today(default) or date as DD/MM/YYYY
            args: up to 3 elements, speifying command, user, channel

        Examples:
            log today homer general: list homer commands in #general channel
            log 05/06/2019 faq: list all moderaiton commands in #faq on 05/06/2019

        """

        # arg_lists is always ["user", "command", "channel"]
        args_list = args_separator_for_log_function(self.bot.guild, args)

        if date == "today":
            date = datetime.date.today().strftime("%d/%m/%Y")

        if self.log.log_read(date, *args_list) is not None:  # if it is None, there are no logs on the given date  # noqa:E501

            # we get a list of tuple in this format [(time,user,command,channel)]
            list_log = self.log.log_read(date, *args_list)  # to avoid multiple calling

            generator = LogsEmbedGenerator(args_list, list_log)
            embed = generator.generate_logs_embed()

            await ctx.author.send(embed=embed)
        else:  # no logs in the given date
            await ctx.author.send(content="Rien dans cette date !")

    @commands.command()
    @commands.is_owner()
    async def log_latest(self, ctx, numb=10):
        """Send latest logs."""
        embed = discord.Embed(title="latest logs")
        latest = self.log.log_latest(int(numb))
        for i in latest:
            embed.add_field(name='\u200B', value=i, inline=False)
        await ctx.author.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def kill(self, ctx):
        """Kill the bot."""
        await self.bot.logout()


class LogsEmbedGenerator():
    """Class to handle generation of logs embed, given arg_list and logs.

    Used in !logs command.

    arg_lists is always ['user', 'command', 'channel']
    """
    def __init__(self, args_list, logs):
        self.user, self.command, self.channel = args_list
        self.logs = logs
        self.n = self._compute_log_case(args_list)  # decimal representation of args array like ["foo", None, None] -> 100 -> 4  # noqa: E501
        self.embed = discord.Embed(title="logs", colour=0xe7191f)

    def _compute_log_case(self, args_list):
        bin_array = [int(i is not None) for i in args_list]  # convert ["foo", None, None] to [1, 0, 0]  # noqa:E501
        return int("".join(str(x) for x in bin_array), 2)  # binary array to int

    def generate_logs_embed(self):
        """Switch/case implementation. Use the right embed generator."""
        return getattr(self, '_gen_' + str(self.n))()

    def _gen_0(self):  # [None, None, None]
        for v in self.logs:
            self.embed.add_field(name=v[0], value=f"{v[1]} used {v[2]} in {v[3]}", inline=False)  # noqa:E501
        return self.embed

    def _gen_1(self):  # [None, None, channel]
        self.embed.set_footer(text=self.channel)
        for v in self.logs:
            self.embed.add_field(name=v[0], value=f"{v[1]} used {v[2]}", inline=False)  # noqa:E501
        return self.embed

    def _gen_2(self):  # [None, command, None]
        self.embed.set_footer(text=f"users of {self.command}")
        for v in self.logs:
            self.embed.add_field(name=v[0], value=f"{v[1]} in {v[2]}", inline=False)  # noqa:E501
        return self.embed

    def _gen_3(self):  # [None, command, channel]
        self.embed.set_footer(text=f"users of {self.command} in {self.channel}")
        for v in self.logs:
            self.embed.add_field(name=v[0], value=f"{v[1]}", inline=False)
        return self.embed

    def _gen_4(self):  # [user, None, None]
        self.embed.set_footer(text=self.user)
        for v in self.logs:
            self.embed.add_field(name=v[0], value=f"used {v[1]} in {v[2]}", inline=False)  # noqa:E501
        return self.embed

    def _gen_5(self):  # [user, None, channel]
        self.embed.set_footer(text=f"{self.user} commands in {self.channel}")
        for v in self.logs:
            self.embed.add_field(name=v[0], value=f"used {v[2]}", inline=False)
        return self.embed

    def _gen_6(self):  # [user, command, None]
        self.embed.set_footer(text=f"{self.user} used {self.command}")
        for v in self.logs:
            self.embed.add_field(name=v[0], value=f"used in {v[2]}", inline=False)  # noqa:E501
        return self.embed

    def _gen_7(self):  # [user, command, channel]
        self.embed.set_footer(text=f"{self.user} used {self.command} in {self.channel}")
        for v in self.logs:
            self.embed.add_field(name=v[0], value=f"{v[1]}", inline=False)
        return self.embed

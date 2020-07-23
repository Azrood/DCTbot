#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module for the ErrorLogs cog."""

import aiohttp
import traceback
import discord
from discord.ext import commands
from utils.secret import logging_webhook_url as secret_webhook


IGNORED_ERRORS = (
    commands.UserInputError,
    commands.DisabledCommand,
    commands.CommandNotFound,
    commands.CheckFailure,
    commands.NoPrivateMessage,
    commands.CommandOnCooldown,
    )


class ErrorLogs(commands.Cog):
    """Log tracebacks of command errors in discord channels."""

    def __init__(self, *args):
        # super().__init__()
        # self.bot = bot
        self.url = secret_webhook

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Fires when a command error occurs and logs them."""
        if isinstance(error, IGNORED_ERRORS):
            return

        # Make Embed
        error_title = f"Exception in command `{ctx.command.qualified_name}`"

        embed = discord.Embed(
            title=error_title,
            colour=discord.Colour.red(),
            timestamp=ctx.message.created_at,
            )
        embed.add_field(name="Invoker", value=f"{ctx.author.mention}\n{ctx.author}\n")  # noqa: E501
        embed.add_field(name="Content", value=ctx.message.content)
        _channel_disp = (
            "{}\n({})".format(ctx.channel.mention, ctx.channel.name)
            if ctx.guild is not None
            else str(ctx.channel)
        )
        embed.add_field(name="Channel", value=_channel_disp)

        if ctx.guild is not None:
            embed.add_field(name="Server", value=ctx.guild.name)

        data = {"embeds": [embed.to_dict()]}

        # Traceback :
        log = "".join(traceback.format_exception(type(error), error, error.__traceback__))  # noqa: E501

        # Send log with Discord webhook url
        async with aiohttp.ClientSession() as session:
            await session.post(self.url, json=data, timeout=3)

            await session.post(self.url,
                               json={'content': "```\n" + log + "```"},
                               timeout=3)

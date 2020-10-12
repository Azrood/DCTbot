import pytest

from discord.ext import commands
import discord.ext.test as dpytest

from utils.tools import args_separator_for_log_function


@pytest.mark.asyncio
async def test_args_separator(bot):

    user = "TestUser0"
    command = "ban"
    channel = "Channel_0"

    dpytest.configure(bot)

    guild = bot.guilds[0]
    a, b, c = args_separator_for_log_function(guild, [channel, command, user])

    assert a == user.lower()
    assert b == command.lower()
    assert c == channel.lower()

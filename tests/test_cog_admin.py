# import asyncio
import pytest
from unittest import mock

import discord
from discord.ext import commands
import discord.ext.test as dpytest

from cogs import Admin


@pytest.mark.asyncio
async def test_restart_fail():
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.gifs = []
    bot.log = mock.Mock()
    bot.add_cog(Admin(bot))
    dpytest.configure(bot)
    # MissingAnyRole is expected.
    # Test will pass if error "MissingAnyRole" is launched
    with pytest.raises(commands.MissingAnyRole):
        await dpytest.message('!restart')
    dpytest.verify_message("Nope.")  # empty the queue
    await dpytest.empty_queue()

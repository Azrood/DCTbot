# import asyncio
import pytest
import pytest_asyncio
from unittest import mock

from discord.ext import commands
import discord.ext.test as dpytest

from cogs import Admin


#########################
# Fixtures
#########################

@pytest_asyncio.fixture(autouse=True)
async def bot_misc(bot):
    bot.gifs = []
    bot.log = mock.Mock()
    await bot.add_cog(Admin(bot))
    dpytest.configure(bot)
    return bot


#########################
# Tests
#########################

@pytest.mark.asyncio
async def test_restart_fail():
    # MissingAnyRole is expected.
    # Test will pass if error "MissingAnyRole" is launched
    with pytest.raises(commands.MissingAnyRole):
        await dpytest.message('!restart')
    assert dpytest.verify().message().content("Nope.")

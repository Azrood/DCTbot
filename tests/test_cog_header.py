import pytest
import pytest_asyncio
import re

import discord.ext.test as dpytest

from cogs import Header


#########################
# Fixtures
#########################

# fixture for bot with Header cog loaded will be used in all tests of the file.
@pytest_asyncio.fixture(autouse=True)
async def bot_header(bot):
    await bot.add_cog(Header(bot))
    dpytest.configure(bot)
    return bot


#########################
# Tests
#########################

@pytest.mark.asyncio
@pytest.mark.parametrize("editor", ["rebirth", "horsrebirth", "inde", "marvel"])
async def test_command_header(bot, editor):

    await dpytest.message(f'!header {editor}')
    attach = dpytest.get_message().attachments[0]
    # assert embed.title == "Comics du mois"
    assert re.match(r'header\d-\d+-\d+.jpg', attach.filename)

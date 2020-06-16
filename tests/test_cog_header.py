import pytest
import re
# # import discord
from discord.ext import commands
import discord.ext.test as dpytest

from cogs import Header


#########################
# Fixtures
#########################

# fixture for bot with Header cog loaded will be used in all tests of the file.
@pytest.fixture(autouse=True)
def bot_header(bot):
    bot.add_cog(Header(bot))
    dpytest.configure(bot)
    return bot


#########################
# Tests
#########################

@pytest.mark.asyncio
@pytest.mark.parametrize("editor", ["rebirth", "horsrebirth", "indé", "marvel"])
async def test_command_header(editor):
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Header(bot))
    dpytest.configure(bot)

    await dpytest.message(f'!header {editor}')
    response = dpytest.runner.sent_queue.get_nowait()
    embed = response.embeds[0]
    attach = response.attachments[0]
    assert embed.title == "Comics du mois"
    assert re.match(r'header\d-\d+-\d+.jpg', attach.filename)

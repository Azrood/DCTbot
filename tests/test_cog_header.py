import pytest
import re
# # import discord
from discord.ext import commands
import discord.ext.test as dpytest

from cogs import Header


@pytest.mark.asyncio
async def test_command_header():
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Header(bot))
    dpytest.configure(bot)

    test_cases = ["rebirth", "horsrebirth", "indé", "marvel"]

    for test in test_cases:
        await dpytest.message(f'!header {test}')
        response = dpytest.runner.sent_queue.get_nowait()
        embed = response.embeds[0]
        attach = response.attachments[0]
        assert embed.title == "Comics du mois"
        assert re.match(r'header\d-\d+-\d+.jpg', attach.filename)

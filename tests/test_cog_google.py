import pytest
# from unittest import mock
# import discord
from discord.ext import commands
import discord.ext.test as dpytest

from cogs import google


@pytest.fixture
def search_result():
    return [{"title": "Python Docs",
             "url": "https://docs.python.org/"},
            {"title": "Documentation - Our Documentation | Python.org",
             "url": "https://www.python.org/doc/"}]


@pytest.fixture(autouse=True)
def mock_response(monkeypatch, search_result):

    async def mock_resp(*args, **kwargs):
        return search_result

    monkeypatch.setattr(google, "search_google", mock_resp)


@pytest.mark.asyncio
async def test_command_google():
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(google.Google(bot))
    dpytest.configure(bot)

    await dpytest.message('!google python doc')
    dpytest.verify_message("Python Docs\n https://docs.python.org/")


@pytest.mark.asyncio
async def test_command_google_list(search_result):
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(google.Google(bot))
    dpytest.configure(bot)
    await dpytest.message('!googlelist 2 python doc')
    res = dpytest.runner.sent_queue.get_nowait().embeds[0]
    assert res.fields[0].name == search_result[0]['title']
    assert res.fields[0].value == search_result[0]['url']
    assert res.fields[1].name == search_result[1]['title']
    assert res.fields[1].value == search_result[1]['url']
    assert len(res.fields) == len(search_result)

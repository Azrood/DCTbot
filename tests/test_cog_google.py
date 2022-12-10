import pytest
import pytest_asyncio
# from unittest import mock
import discord
import discord.ext.test as dpytest

from cogs import google


#########################
# Fixtures
#########################

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


@pytest.fixture
def expected_embed(search_result):
    embed = discord.Embed(title="Les 2 premiers résultats de la recherche",
                          color=0x3b5cbe)
    for r in search_result:
        embed.add_field(name=r['title'], value=r['url'], inline=False)

    return embed


# fixture for bot with Google cog loaded will be used in all tests of the file.
@pytest_asyncio.fixture(autouse=True)
async def bot_google(bot):
    await bot.add_cog(google.Google(bot))
    dpytest.configure(bot)
    return bot


#########################
# Tests
#########################

@pytest.mark.asyncio
async def test_command_google():

    await dpytest.message('!google python doc')
    assert dpytest.verify().message().content("Python Docs\n https://docs.python.org/")


@pytest.mark.asyncio
async def test_command_google_list(expected_embed):

    await dpytest.message('!googlelist 2 python doc')
    assert dpytest.verify().message().embed(expected_embed)

import pytest
import pytest_asyncio

import discord
from discord.ext import commands
import discord.ext.test as dpytest

from cogs import Gifs
from utils.gif_json import GifJson


#########################
# Fixtures
#########################

@pytest.fixture(scope='module')
def gifs():
    return {"foo": {"public": True, "url": "http://foo.gif"},
            "bar": {"public": True, "url": "http://bar.gif"},
            "foobar": {"public": False, "url": "http://foobar.gif"}}


@pytest.fixture(scope='module')
def gifs_json(gifs):
    gif_json = GifJson("gifs.sample.json")
    gif_json.gifs = gifs
    return gif_json


@pytest.fixture(scope='module')
def expected_foo_embed(gifs):
    embed = discord.Embed()
    embed.set_image(url=gifs['foo']['url'])
    return embed


# fixture for bot with Gifs cog loaded will be used in all tests of the file.
@pytest_asyncio.fixture(autouse=True)
async def bot_gifs(bot, gifs_json):
    await bot.add_cog(Gifs(bot))
    bot.gifs = gifs_json
    bot.prefix = '!'
    dpytest.configure(bot)
    return bot


#########################
# Tests
#########################

@pytest.mark.asyncio
async def test_command_gif(expected_foo_embed):

    await dpytest.message('!gif foo')
    assert dpytest.verify().message().embed(expected_foo_embed)


@pytest.mark.asyncio
async def test_command_gif_in_public():
    """Test call to a private gif in a public channel."""

    await dpytest.message('!gif foobar')
    assert dpytest.verify().message().nothing()


@pytest.mark.asyncio
async def test_on_message_gif(expected_foo_embed):

    try:
        await dpytest.message('!foo')
    except commands.errors.CommandNotFound:
        pass
    finally:
        assert dpytest.verify().message().embed(expected_foo_embed)


@pytest.mark.asyncio
async def test_command_gif_help():

    expected_embed = discord.Embed(title="liste des gifs",
                                   description="foo\nbar",
                                   color=0x000FF)

    await dpytest.message('!gif help')
    assert dpytest.verify().message().embed(expected_embed)

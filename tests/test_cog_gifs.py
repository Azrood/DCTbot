import pytest

import discord
from discord.ext import commands
import discord.ext.test as dpytest

from cogs import Gifs
from utils.gif_json import GifJson


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


@pytest.mark.asyncio
async def test_command_gif(gifs_json, expected_foo_embed):
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Gifs(bot))

    bot.gifs = gifs_json

    dpytest.configure(bot)
    await dpytest.message('!gif foo')
    dpytest.verify_embed(expected_foo_embed)


@pytest.mark.asyncio
async def test_command_gif_in_public(gifs_json, expected_foo_embed):
    """Test call to a private gif in a public channel."""
    bot = commands.Bot(command_prefix='!')
    bot.prefix = '!'
    bot.add_cog(Gifs(bot))

    bot.gifs = gifs_json

    dpytest.configure(bot)
    await dpytest.message('!gif foobar')
    dpytest.verify_embed(assert_nothing=True)


@pytest.mark.asyncio
async def test_on_message_gif(gifs_json, expected_foo_embed):
    bot = commands.Bot(command_prefix='!')
    bot.prefix = '!'
    bot.add_cog(Gifs(bot))

    bot.gifs = gifs_json

    try:
        dpytest.configure(bot)
        await dpytest.message('!foo')
    except commands.errors.CommandNotFound:
        pass
    finally:
        dpytest.verify_embed(expected_foo_embed)


@pytest.mark.asyncio
async def test_command_gif_help(gifs_json):
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Gifs(bot))

    bot.gifs = gifs_json

    expected_embed = discord.Embed(title="liste des gifs",
                                   description="foo\nbar",
                                   color=0x000FF)

    dpytest.configure(bot)
    await dpytest.message('!gif help')
    dpytest.verify_embed(expected_embed)

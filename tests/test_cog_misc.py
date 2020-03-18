import asyncio
import pytest
# from unittest import mock

import random

import discord
from discord.ext import commands
import discord.ext.test as dpytest

from cogs import Misc


@pytest.mark.asyncio
async def test_ping():
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Misc(bot))
    dpytest.configure(bot)
    await dpytest.message('!ping')
    dpytest.verify_message("pong !")


@pytest.mark.asyncio
async def test_say():
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Misc(bot))
    dpytest.configure(bot)
    await dpytest.message('!say Unit testing the say command')
    dpytest.verify_message("Unit testing the say command")


@pytest.mark.asyncio
async def test_recrutement():
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Misc(bot))
    dpytest.configure(bot)

    await dpytest.message('!recrutement')

    expected_embed = discord.Embed(title='Rejoins la team DCTrad !',
                                   description="allez n'aie pas peur de cliquer et deviens un héros !",
                                   color=0x0000FF,
                                   url="http://www.dctrad.fr/viewforum.php?f=21")  # noqa: E501

    dpytest.verify_embed(expected_embed)


@pytest.mark.asyncio
async def test_choose(monkeypatch):
    """Test of random choice (with monkey patching)"""

    def mock_choice(*args, **kwargs):
        return "toto"

    monkeypatch.setattr(random, "choice", mock_choice)
    # TODO:
    # I think we can do simpler than that, with a decorator (mock.patch ?)
    # to know more, please see :
    # https://docs.pytest.org/en/latest/monkeypatch.html

    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Misc(bot))
    dpytest.configure(bot)
    await dpytest.message('!choose toto tat tutu TITI')

    dpytest.verify_message("toto")


@pytest.mark.asyncio
async def test_coinflip(monkeypatch):

    def mock_coin(*args, **kwargs):
        return "pile"

    monkeypatch.setattr(random, "choice", mock_coin)
    # TODO:
    # I think we can do simpler than that, with a decorator (mock.patch ?)
    # to know more, please see :
    # https://docs.pytest.org/en/latest/monkeypatch.html

    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Misc(bot))
    dpytest.configure(bot)
    await dpytest.message('!coinflip')

    dpytest.verify_message("pile")


@pytest.mark.asyncio
async def test_roulette_lives(monkeypatch):
    """
    Test !roulette (user survives).

    We monkeypatch random so the user always survives.
    """
    alive_mess = "Ouh c'était chaud !"

    def mock_randint(*args, **kwargs):
        return 1

    def mock_choice(*args, **kwargs):
        return alive_mess

    monkeypatch.setattr(random, "randrange", mock_randint)
    monkeypatch.setattr(random, "choice", mock_choice)

    # TODO:
    # I think we can do simpler than that, with a decorator (mock.patch ?)
    # to know more, please see :
    # https://docs.pytest.org/en/latest/monkeypatch.html

    my_bot = commands.Bot(command_prefix='!')
    my_bot.add_cog(Misc(my_bot))
    dpytest.configure(my_bot)
    await dpytest.message('!roulette')
    dpytest.verify_message(alive_mess)


@pytest.mark.asyncio
async def test_roulette_dies(monkeypatch):
    """
    Test !roulette (user dies).

    We monkeypatch random so the user always get kicked.
    """
    dead_mess = "Pan !"
    dead_gif = "https://media.tenor.com/images/8d7d2e757f934793bb4154cede8a4afa/tenor.gif"  # noqa: E501

    def mock_randint(*args, **kwargs):
        return 3

    def mock_choice(*args, **kwargs):
        return dead_mess

    async def mock_sleep(*args, **kwargs):
        return

    monkeypatch.setattr(random, "randrange", mock_randint)  # random will always return 3  # noqa: E501
    monkeypatch.setattr(random, "choice", mock_choice)
    monkeypatch.setattr(asyncio, "sleep", mock_sleep)  # bypass asyncio.sleep

    # TODO:
    # I think we can do simpler than that, with a decorator (mock.patch ?)
    # to know more, please see :
    # https://docs.pytest.org/en/latest/monkeypatch.html

    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Misc(bot))
    dpytest.configure(bot)
    await dpytest.message('!roulette')
    dpytest.verify_message(dead_mess)
    dpytest.verify_message(dead_gif)


@pytest.mark.asyncio
async def test_timer(monkeypatch):

    test_time = 15
    test_message = "wake up"

    async def mock_sleep(*args, **kwargs):
        return

    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Misc(bot))
    dpytest.configure(bot)

    monkeypatch.setattr(asyncio, "sleep", mock_sleep)  # bypass asyncio.sleep

    await dpytest.message(f'!timer {test_time} {test_message}')

    mention = bot.users[0].mention
    dpytest.verify_message(f"{mention} : timer enregistré !")
    dpytest.verify_message(f"temps écoulé ! : {mention} {test_message}")

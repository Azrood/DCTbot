import pytest

import discord
import discord.ext.test as dpytest

from cogs import Misc


#########################
# Fixtures
#########################

# fixture for bot with Misc cog loaded will be used in all tests of the file.
@pytest.fixture(autouse=True)
def bot_misc(bot):
    bot.add_cog(Misc(bot))
    dpytest.configure(bot)
    return bot


#########################
# Tests
#########################

@pytest.mark.asyncio
async def test_ping():
    await dpytest.message('!ping')
    assert dpytest.verify().message().content("pong !")


@pytest.mark.asyncio
async def test_say():
    await dpytest.message('!say Unit testing the say command')
    assert dpytest.verify().message().content("Unit testing the say command")


@pytest.mark.asyncio
async def test_recrutement():
    await dpytest.message('!recrutement')

    expected_embed = discord.Embed(title='Rejoins la team DCTrad !',
                                   description="allez n'aie pas peur de cliquer et deviens un héros !",
                                   color=0x0000FF,
                                   url="http://www.dctrad.fr/viewforum.php?f=21")  # noqa: E501

    assert dpytest.verify().message().embed(expected_embed)


@pytest.mark.asyncio
async def test_choose(monkeypatch):
    """Test of random choice (with monkey patching)"""

    monkeypatch.setattr("random.choice", lambda *args: "toto")

    await dpytest.message('!choose toto tat tutu TITI')
    assert dpytest.verify().message().content("toto")


@pytest.mark.asyncio
async def test_coinflip(monkeypatch):

    monkeypatch.setattr("random.choice", lambda *args: "pile")

    await dpytest.message('!coinflip')
    assert dpytest.verify().message().content("pile")


@pytest.mark.asyncio
async def test_roulette_lives(monkeypatch):
    """
    Test !roulette (user survives).

    We monkeypatch random so the user always survives.
    """
    alive_mess = "Ouh c'était chaud !"

    # Monkeypatching random
    monkeypatch.setattr("random.randrange", lambda *args: 1)
    monkeypatch.setattr("random.choice", lambda *args: alive_mess)

    await dpytest.message('!roulette')
    assert dpytest.verify().message().content(alive_mess)


@pytest.mark.asyncio
async def test_roulette_dies(monkeypatch, mock_sleep):
    """
    Test !roulette (user dies).

    We monkeypatch random so the user always get kicked.
    """
    dead_mess = "Pan !"
    dead_gif = "https://media.tenor.com/images/8d7d2e757f934793bb4154cede8a4afa/tenor.gif"  # noqa: E501

    # Monkeypatching random
    monkeypatch.setattr("random.randrange", lambda *args: 3)  # random will always return 3  # noqa: E501
    monkeypatch.setattr("random.choice", lambda *args: dead_mess)

    await dpytest.message('!roulette')
    assert dpytest.verify().message().content(dead_mess)
    assert dpytest.verify().message().content(dead_gif)


# In this test, we use a fixture to monkeypatch asyncio.sleep
@pytest.mark.asyncio
async def test_timer(bot, mock_sleep):

    test_time = 15
    test_message = "wake up"
    mention = bot.users[0].mention.replace("@", "@!")

    await dpytest.message(f'!timer {test_time} {test_message}')

    assert dpytest.verify().message().content(f"{mention} : timer enregistré !")
    assert dpytest.verify().message().content(f"temps écoulé ! : {mention} {test_message}")

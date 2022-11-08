# import asyncio
import pytest
# from unittest import mock

import discord
import discord.ext.test as dpytest

from cogs import Cards


#########################
# Fixtures
#########################

# fixture for bot with Cards cog loaded will be used in all tests of the file.
@pytest.fixture(autouse=True)
def bot_cards(bot):
    bot.add_cog(Cards(bot))
    dpytest.configure(bot)
    return bot


#########################
# Tests
#########################

@pytest.mark.asyncio
async def test_card():
    expected = discord.Embed()
    expected.set_image(url="attachment://sergei.jpg")

    await dpytest.message('!poke sergei')
    assert dpytest.verify().message().embed(expected)


@pytest.mark.asyncio
async def test_card_help():
    expected = discord.Embed(title="Liste des cartes \nSyntaxe : !poke <nom>",
                             description="azrod\nbane\nrun\nsergei\nxanatos\nphoe")  # noqa: E501
    expected.set_footer(text="Merci à Slyrax pour les cartes !")

    await dpytest.message('!poke help')
    assert dpytest.verify().message().embed(expected)

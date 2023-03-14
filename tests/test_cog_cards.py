# import asyncio
import pytest
import pytest_asyncio
# from unittest import mock
from pathlib import Path

import discord
import discord.ext.test as dpytest

from cogs import Cards


#########################
# Fixtures
#########################

# fixture for bot with Cards cog loaded will be used in all tests of the file.
@pytest_asyncio.fixture(autouse=True)
async def bot_cards(bot):
    await bot.add_cog(Cards(bot))
    dpytest.configure(bot)
    return bot


#########################
# Tests
#########################

@pytest.mark.asyncio
async def test_card():
    path_ = Path(__file__).resolve().parents[1] / "pictures" / "cards" / "sergei.jpg"  # noqa: E501

    await dpytest.message('!poke sergei')
    assert dpytest.verify().message().attachment(path_)


@pytest.mark.asyncio
async def test_card_help():
    cards_dir = Path(__file__).resolve().parents[1] / "pictures" / "cards"
    cards_list = [child.stem for child in cards_dir.iterdir()]

    expected = discord.Embed(title="Liste des cartes \nSyntaxe : !poke <nom>",
                             description='\n'.join(cards_list))  # noqa: E501
    expected.set_footer(text="Merci à Slyrax pour les cartes !")

    await dpytest.message('!poke help')
    assert dpytest.verify().message().embed(expected)

# import asyncio
import pytest
# from unittest import mock

import discord
from discord.ext import commands
import discord.ext.test as dpytest

from cogs import Cards


@pytest.mark.asyncio
async def test_card():
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Cards(bot))
    dpytest.configure(bot)

    expected = discord.Embed()
    expected.set_image(url="attachment://sergei.jpg")

    await dpytest.message('!poke sergei')
    dpytest.verify_embed(expected)


@pytest.mark.asyncio
async def test_card_help():
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(Cards(bot))
    dpytest.configure(bot)

    expected = discord.Embed(title="Liste des cartes \nSyntaxe : !poke <nom>",
                             description="azrod\nbane\nrun\nsergei\nxanatos\nphoe")  # noqa: E501
    expected.set_footer(text="Merci à Slyrax pour les cartes !")

    await dpytest.message('!poke help')
    dpytest.verify_embed(expected)

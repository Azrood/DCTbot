# import asyncio
import pytest
# from unittest import mock

import discord
from discord.ext import commands
import discord.ext.test as dpytest

from cogs import Help  # noqa: F401
from utils.constants import helps
from utils.secret import staff_role, mods_role


@pytest.fixture()
def expected_embed():
    embed = discord.Embed(
        title="Page 1/2, utilisez les flèches en réaction pour naviguer",
        description="Liste des commandes(toutes les commandes doivent être précédées du prefix \"!\") :",  # noqa: E501
        color=0x0000FF)

    # Add fields
    for s in helps:
        if len(embed.fields) < 10:
            embed.add_field(name=s['name'], value=s['value'], inline=False)

    return embed


@pytest.mark.asyncio
async def test_help(expected_embed):
    team_role_name = staff_role[0]  # DCT-team
    modo_role_name = mods_role[0]  # Moderator
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    dpytest.configure(bot)

    guild = bot.guilds[0]  # Guild object
    team_role = await guild.create_role(name=team_role_name)  # Role object
    modo_role = await guild.create_role(name=modo_role_name)  # Role object
    bot.role_dcteam = modo_role
    bot.role_modo = team_role

    # bot.add_cog(Help(bot))  # Error saying command help is already registered ???  # noqa: E501

    # TODO : wait until this test can be performed, and uncomment next line
    # await dpytest.message('!help')  # delete and stuffs not implemented yet

    # TODO:
    # assert embed is expected_emebed

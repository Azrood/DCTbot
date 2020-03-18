# import asyncio
import pytest
# from unittest import mock

# import discord
from discord.ext import commands
import discord.ext.test as dpytest

from cogs import Mod
from utils.logs import CommandLog
from utils.secret import mods_role


# @pytest.mark.asyncio
# async def test_kick_fail():
#     modo_role_name = mods_role[0]  # DCT-team

#     bot = commands.Bot(command_prefix='!')
#     dpytest.configure(bot, num_members=2)

#     bot.log = CommandLog("test_log.json")

#     guild = bot.guilds[0]  # Guild object
#     modo_role = await guild.create_role(name=modo_role_name)  # Role object
#     bot.role_dcteam = modo_role
#     member1 = guild.members[0]  # Member
#     member2 = guild.members[1]  # Member

#     m1_mention = member1.mention
#     m2_mention = member2.mention

#     bot.add_cog(Mod(bot))

#     with pytest.raises(commands.MissingAnyRole):
#         await dpytest.message(f'!kick {m2_mention}')

#     dpytest.verify_message(f"Tu n'as pas de pouvoirs{m1_mention} !")
#     dpytest.empty_queue()
#     print("toto")


@pytest.mark.asyncio
async def test_kick_success():
    modo_role_name = mods_role[0]  # Moderator

    bot = commands.Bot(command_prefix='!')
    dpytest.configure(bot, num_members=2)

    bot.log = CommandLog("test_log.json")

    guild = bot.guilds[0]  # Guild object
    modo_role = await guild.create_role(name=modo_role_name)  # Role object
    bot.role_modo = modo_role
    member1 = guild.members[0]  # Member
    member2 = guild.members[1]  # Member

    # m1_mention = member1.mention
    m2_mention = member2.mention

    bot.add_cog(Mod(bot))

    await member1.add_roles(modo_role)  # m1 has the role Moderator

    assert len(guild.members) == 3  # member1, member2 and the bot

    await dpytest.message(f'!kick {m2_mention}')

    dpytest.verify_message("Adios muchachos !")
    assert len(guild.members) == 2  # member1 and the bot

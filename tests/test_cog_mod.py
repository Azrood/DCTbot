import pytest
# from unittest import mock

from discord.ext import commands
import discord.ext.test as dpytest

from cogs import Mod
from utils.logs import CommandLog
from utils.secret import mods_role


@pytest.mark.asyncio
async def test_kick_fail(bot):
    dpytest.configure(bot, num_members=2)
    bot.log = CommandLog("test_log.json")
    await bot.add_cog(Mod(bot))
    modo_role_name = mods_role[0]  # Moderator
    guild = bot.guilds[0]  # Guild object
    modo_role = await guild.create_role(name=modo_role_name)  # Role object
    bot.role_modo = modo_role
    member1 = guild.members[0]  # Member
    member2 = guild.members[1]  # Member
    m1_mention = member1.mention
    m2_mention = member2.mention

    with pytest.raises(commands.MissingAnyRole):
        await dpytest.message(f'!kick {m2_mention}')

    assert dpytest.verify().message().content(f"Tu n'as pas de pouvoirs{m1_mention} !")  # noqa: E501


@pytest.mark.asyncio
async def test_kick_success(bot):
    dpytest.configure(bot, num_members=2)
    bot.log = CommandLog("test_log.json")
    await bot.add_cog(Mod(bot))

    modo_role_name = mods_role[0]  # Moderator
    guild = bot.guilds[0]  # Guild object
    modo_role = await guild.create_role(name=modo_role_name)  # Role object
    bot.role_modo = modo_role
    member1 = guild.members[0]  # Member
    member2 = guild.members[1]  # Member

    m2_mention = member2.mention

    await member1.add_roles(modo_role)  # m1 has the role Moderator

    assert len(guild.members) == 3  # member1, member2 and the bot

    await dpytest.message(f'!kick {m2_mention}')

    assert dpytest.verify().message().content("Adios muchachos !")
    assert len(guild.members) == 2  # member1 and the bot

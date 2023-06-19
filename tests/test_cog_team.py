import pytest

from discord.ext import commands
import discord.ext.test as dpytest

from cogs import Team
from utils.logs import CommandLog
from utils.secret import staff_role


@pytest.mark.asyncio
async def test_team_fail(bot):
    team_role_name = staff_role[0]  # DCT-team

    guild = bot.guilds[0]  # Guild object
    team_role = await guild.create_role(name=team_role_name)  # Role object
    bot.role_dcteam = team_role
    # member1 = guild.members[0]  # Member

    bot.log = CommandLog("test_log.json")

    await bot.add_cog(Team(bot))

    member2 = guild.members[1]  # Member

    m2_mention = member2.mention

    with pytest.raises(commands.MissingAnyRole):
        await dpytest.message(f'!team {m2_mention}')  # m1 gives m2 a new role

    # After
    assert team_role not in member2.roles  # m2 has NOT the role
    assert dpytest.verify().message().content("Bien tenté mais tu n'as pas de pouvoir ici !")  # noqa: E501


@pytest.mark.asyncio
async def test_team_success(bot):
    team_role_name = staff_role[0]  # DCT-team

    dpytest.configure(bot, members=2)

    bot.log = CommandLog("test_log.json")

    guild = bot.guilds[0]  # Guild object
    team_role = await guild.create_role(name=team_role_name)  # Role object
    bot.role_dcteam = team_role
    member1 = guild.members[0]  # Member
    member2 = guild.members[1]  # Member

    m2_mention = member2.mention

    await bot.add_cog(Team(bot))

    # Before command
    assert team_role not in member2.roles  # m2 doesn't have the role

    await member1.add_roles(team_role)  # m1 has the role Team

    await dpytest.message(f'!team {m2_mention}')  # m1 gives m2 a new role

    # After
    assert team_role in member2.roles  # m2 has the role
    assert dpytest.verify().message().content("Bienvenue dans la Team !")


@pytest.mark.asyncio
async def test_team_empty_mentions(bot):
    """Test "team!" command with no mentions."""
    team_role_name = staff_role[0]  # DCT-team

    dpytest.configure(bot, members=2)

    bot.log = CommandLog("test_log.json")

    guild = bot.guilds[0]  # Guild object
    team_role = await guild.create_role(name=team_role_name)  # Role object
    bot.role_dcteam = team_role
    member1 = guild.members[0]  # Member
    member2 = guild.members[1]  # Member

    await bot.add_cog(Team(bot))

    # Before command
    assert team_role not in member2.roles  # m2 doesn't have the role

    await member1.add_roles(team_role)  # m1 has the role Team

    # test empty mentions -> nothing happens
    await dpytest.message('!team')
    assert dpytest.verify().message().nothing()


@pytest.mark.asyncio
async def test_team_member_allready_in_team(bot):
    """Test !team with one member allready in team."""
    team_role_name = staff_role[0]  # DCT-team

    dpytest.configure(bot, members=3)

    bot.log = CommandLog("test_log.json")

    guild = bot.guilds[0]  # Guild object
    team_role = await guild.create_role(name=team_role_name)  # Role object
    bot.role_dcteam = team_role
    member1 = guild.members[0]  # Member
    member2 = guild.members[1]  # Member
    member3 = guild.members[2]  # Member

    m2_mention = member2.mention
    m3_mention = member3.mention

    await bot.add_cog(Team(bot))

    await member1.add_roles(team_role)  # m1 has the role Team
    await member2.add_roles(team_role)  # m2 has the role Team

    # Before command
    assert team_role not in member3.roles  # m2 doesn't have the role

    # test empty mentions -> nothing happens
    await dpytest.message('!team')
    assert dpytest.verify().message().nothing()

    await dpytest.message(f'!team {m2_mention} {m3_mention}')  # m1 gives m2 a new role

    # After
    assert team_role in member3.roles  # m3 has the role
    assert dpytest.verify().message().content("Bienvenue dans la Team !")


@pytest.mark.asyncio
async def test_clear_fail(bot):
    team_role_name = staff_role[0]  # DCT-team

    dpytest.configure(bot)

    bot.log = CommandLog("test_log.json")

    # await dpytest.message("message 1")
    # await dpytest.message("message 2")
    # await dpytest.message("message 3")

    # last_message = bot.guilds[0].channels[0].last_message.content

    # assert last_message == "message 3"

    guild = bot.guilds[0]  # Guild object
    team_role = await guild.create_role(name=team_role_name)  # Role object
    bot.role_dcteam = team_role

    member_mention = guild.members[0].mention  # Member

    await bot.add_cog(Team(bot))

    with pytest.raises(commands.MissingAnyRole):
        await dpytest.message("!clear 2")
    assert dpytest.verify().message().content(f"Tu n'as pas le pouvoir{member_mention} !")  # noqa: 501

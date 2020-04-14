import pytest
# from unittest import mock
import discord
import discord.ext.test as dpytest

from cogs import Urban


#########################
# Fixtures
#########################

@pytest.fixture()
def expected_embed():
    embed = discord.Embed(title="Definition of Distro Hop",
                          description='The act of switching from one linux distro to another.'[:2048],  # noqa: E501
                          color=0x00FFFF,
                          url='https://www.urbandictionary.com/define.php?term=distro+hop')  # noqa: E501
    embed.add_field(name="Example", value='No example'[:2048], inline=False)
    # embed.set_thumbnail(url=urban_logo)
    return embed


# fixture for bot with Urban cog loaded will be used in all tests of the file.
@pytest.fixture(autouse=True)
def bot_urban(bot):
    bot.add_cog(Urban(bot))
    dpytest.configure(bot)
    return bot


#########################
# Tests
#########################

@pytest.mark.asyncio
async def test_urban_cog(expected_embed):

    await dpytest.message('!urban distro hop')
    dpytest.verify_embed(expected_embed)


@pytest.mark.asyncio
async def test_urban_cog_fails():

    user_input = "mlksjdfmlkjsdfmlkjsdf"
    embed = discord.Embed(title=f"Definition of {user_input} doesn't exist")  # noqa: E501

    await dpytest.message(f'!urban {user_input}')
    dpytest.verify_embed(embed)

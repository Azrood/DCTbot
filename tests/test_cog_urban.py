import pytest
import pytest_asyncio

import discord
import discord.ext.test as dpytest

from cogs import Urban


#########################
# Fixtures
#########################

@pytest.fixture()
def expected_embed():
    expected = discord.Embed(title="Definition of Distro Hop",
                             description="The act of switching from one linux distro to another."[:2048],  # noqa: E501
                             color=0x00FFFF,
                             url="https://www.urbandictionary.com/define.php?term=distro%20hop")  # noqa: E501
    expected.add_field(name="Example",
                       value="I just Distro Hopped from Arch KDE to Gentoo i3"[:2048],
                       inline=False)
    # embed.set_thumbnail(url=urban_logo)
    return expected


# fixture for bot with Urban cog loaded will be used in all tests of the file.
@pytest_asyncio.fixture(autouse=True)
async def bot_urban(bot):
    await bot.add_cog(Urban(bot))
    dpytest.configure(bot)
    return bot


#########################
# Tests
#########################

@pytest.mark.asyncio
async def test_urban_cog(expected_embed: discord.Embed):
    await dpytest.message('!urban distro hop')
    assert dpytest.verify().message().embed(expected_embed)


@pytest.mark.asyncio
async def test_urban_cog_fails():
    user_input = "mlksjdfmlkjsdfmlkjsdf"
    embed = discord.Embed(title=f"Definition of {user_input} doesn't exist")  # noqa: E501

    await dpytest.message(f'!urban {user_input}')
    assert dpytest.verify().message().embed(embed)

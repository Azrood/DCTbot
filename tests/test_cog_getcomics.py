import pytest
# from unittest import mock
import discord
import discord.ext.test as dpytest

from cogs import getcomics


#########################
# Fixtures
#########################

@pytest.fixture()
def expected_embed():
    embed = discord.Embed(title="Batman #80 (2019)", color=0x882640,
                          description="cliquez sur le titre pour télécharger votre comic",  # noqa: E501
                          url="https://getcomics.info/dc/batman-80-2019/")  # noqa: E501)
    embed.set_image(url="https://i0.wp.com/getcomics.info/share/uploads/2019/09/Batman-80-2019.jpg")
    return embed


@pytest.fixture(autouse=True)  # turn to True to test when offline
def mock_response(monkeypatch):

    async def mocked_values(*args, **kwargs):
        title = "Batman #80 (2019)"
        url = "https://getcomics.info/dc/batman-80-2019/"
        cover = "https://i0.wp.com/getcomics.info/share/uploads/2019/09/Batman-80-2019.jpg"  # noqa: E501
        return title, url, cover

    monkeypatch.setattr(getcomics, "getcomics_top_link", mocked_values)


#########################
# Tests
#########################

@pytest.mark.asyncio
async def test_getcomics(bot, expected_embed):
    bot.add_cog(getcomics.Getcomics(bot))
    dpytest.configure(bot)
    await dpytest.message('!getcomics batman #80')
    assert dpytest.verify().message().embed(expected_embed)

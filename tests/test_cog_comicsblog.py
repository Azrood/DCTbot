from pathlib import Path

from bs4 import BeautifulSoup
import pytest
# from unittest import mock
import discord
import discord.ext.test as dpytest

from cogs import comicsblog


DATA_DIR = Path(__file__).parent / "data"


def datafile(filename: str) -> Path:
    return DATA_DIR / filename


#########################
# Fixtures
#########################

@pytest.fixture(autouse=True)
def mock_response(monkeypatch):

    async def mock_resp(*args, **kwargs):
        txt = open(datafile("comicsblog.txt")).read()
        return BeautifulSoup(txt, 'html.parser')

    monkeypatch.setattr(comicsblog, "get_soup_html", mock_resp)


@pytest.fixture()
def expected_values():
    return [
        ["David Mazzucchelli vous explique la grammaire de la BD dans le panel ''Storytelling for Comics''",  # noqa: E501
         "http://www.comicsblog.fr/37653-David_Mazzucchelli_vous_explique_la_grammaire_de_la_BD_dans_le_panel_Storytelling_for_Comics"],  # noqa: E501
        ["Le nouveau Lil' Gotham (Batman Once Upon A Crime) arrive chez Urban Comics en mai 2020",  # noqa: E501
         "http://www.comicsblog.fr/37654-Le_nouveau_Lil_Gotham_Batman_Once_upon_a_Crime_arrive_chez_urban_Comics_en_mai_2020"]
        ]


@pytest.fixture()
def expected_embed(expected_values):
    embed = discord.Embed(title="les 2 derniers articles de comicsblog",
                          color=0xe3951a)
    for i in expected_values:
        embed.add_field(name=i[0], value=i[1], inline=False)
    return embed


#########################
# Tests
#########################

@pytest.mark.asyncio
async def test_get_comicsblog(expected_values):
    """Test get_comicsblog."""

    res = await comicsblog.get_comicsblog(2)

    values = [[res[0].find('title').text, res[0].find('guid').text],
              [res[1].find('title').text, res[1].find('guid').text]]

    # Compare the 4 values to expected ones
    for i in range(2):
        assert values[i][0] == expected_values[i][0]
        assert values[i][1] == expected_values[i][1]


@pytest.mark.asyncio
async def test_comicsblog_command(bot, expected_embed):
    await bot.add_cog(comicsblog.Comicsblog(bot))
    dpytest.configure(bot)

    await dpytest.message('!comicsblog 2')

    assert dpytest.verify().message().embed(expected_embed)

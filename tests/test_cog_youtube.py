# import asyncio
import asynctest
import pytest
# from unittest.mock import MagicMock
import discord
import discord.ext.test as dpytest

from cogs import youtube


#########################
# Fixtures
#########################

# fixture for bot with Youtube cog loaded will be used in all tests of the file.
@pytest.fixture(autouse=True)
def bot_youtube(bot, monkeypatch):
    bot.add_cog(youtube.Youtube(bot))
    dpytest.configure(bot)

    return bot


@pytest.fixture
def one_result():
    return [{'title': 'Never gonna give you up',
             'type': 'video',
             'id': 'dQw4w9WgXcQ'}]


@pytest.fixture
def two_results():
    return [{'title': 'Pastime Paradise',
             'type': 'video',
             'id': '_H3Sv2zad6s'},
            {'title': "Gangsta's Paradise",
             'type': 'video',
             'id': 'fPO76Jlnz6c'}
            ]


@pytest.fixture
def embed_first_result(two_results):
    embed = discord.Embed(color=0xFF0000)
    embed.set_footer(text="Tapez un nombre pour faire votre choix "
                     "ou dites \"cancel\" pour annuler")
    for s in two_results:
        url = youtube.get_youtube_url(s)
        embed.add_field(name=f"{two_results.index(s)+1}.{s['type']}",
                        value=f"[{s['title']}]({url})", inline=False)
    return embed


@pytest.fixture
def embed_two_results(two_results):
    embed = discord.Embed(color=0xFF0000)
    embed.set_footer(text="Tapez un nombre pour faire votre choix "
                     "ou dites \"cancel\" pour annuler")
    for s in two_results:
        url = youtube.get_youtube_url(s)
        embed.add_field(name=f"{two_results.index(s)+1}.{s['type']}",
                        value=f"[{s['title']}]({url})", inline=False)
    return embed


@pytest.fixture
def mock_wait_for(bot_youtube, monkeypatch):
    """bot.wait_for() mocked to return immediately."""

    async def return_now(*args, **kwargs):
        return

    monkeypatch.setattr(bot_youtube, "wait_for", return_now)


@pytest.fixture
def mock_cancel(bot_youtube, monkeypatch):
    """message 'cancel' is mocked."""

    async def cancel_message(*args, **kwargs):
        msg = asynctest.Mock()
        msg.content = "cancel"
        msg.delete = asynctest.CoroutineMock()
        return msg

    monkeypatch.setattr(bot_youtube, "wait_for", cancel_message)


@pytest.fixture
def mock_message_1(bot_youtube, monkeypatch):
    """message '1' is mocked."""

    async def mock_resp(*args, **kwargs):
        msg = asynctest.Mock()
        msg.content = 1
        msg.delete = asynctest.CoroutineMock()
        return msg

    monkeypatch.setattr(bot_youtube, "wait_for", mock_resp)


#########################
# Tests
#########################

@pytest.mark.asyncio
async def test_command_youtube(monkeypatch, mock_wait_for, one_result):

    monkeypatch.setattr(youtube, "search_youtube", lambda *args, **kwargs: one_result)

    await dpytest.message('!youtube never gonna give you up')
    dpytest.verify_message(f"{one_result[0]['title']}\n"
                           f"https://www.youtube.com/watch?v={one_result[0]['id']}")  # noqa: E501


@pytest.mark.asyncio
async def test_command_youtubelist_cancel(monkeypatch, mock_cancel,
                                          two_results, embed_two_results):

    monkeypatch.setattr(youtube, "search_youtube", lambda *args, **kwargs: two_results)  # noqa: E501

    await dpytest.message('!youtubelist 2 pastime paradise')
    dpytest.verify_embed(embed_two_results)

    # mock_cancel fixture monkeypath wait_for, and 'cancel' message is sent.

    dpytest.verify_message("Annulé !")


@pytest.mark.asyncio
async def test_command_youtubelist_not_cancel(monkeypatch, mock_message_1,
                                              two_results, embed_two_results):

    monkeypatch.setattr(youtube, "search_youtube", lambda *args, **kwargs: two_results)  # noqa: E501

    await dpytest.message('!youtubelist 2 pastime paradise')
    dpytest.verify_embed(embed_two_results)

    # mock_message_1 fixture monkeypath wait_for, and '1' message is sent.

    dpytest.verify_message("https://www.youtube.com/watch?v=_H3Sv2zad6s")

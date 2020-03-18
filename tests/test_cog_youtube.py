# import asyncio
import asynctest
import pytest
# from unittest.mock import MagicMock
# import discord
from discord.ext import commands
import discord.ext.test as dpytest

from cogs import youtube


@pytest.mark.asyncio
async def test_command_youtube(monkeypatch):
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(youtube.Youtube(bot))
    dpytest.configure(bot)

    def mock_resp(*args, **kwargs):
        return [{'title': 'Never gonna give you up',
                 'type': 'video',
                 'id': 'dQw4w9WgXcQ'}]

    async def mock_pass(*args, **kwargs):
        return

    monkeypatch.setattr(youtube, "search_youtube", mock_resp)
    monkeypatch.setattr(bot, "wait_for", mock_pass)

    await dpytest.message('!youtube never gonna give you up')
    res = dpytest.runner.sent_queue.get_nowait()
    assert res.content == 'Never gonna give you up\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ'  # noqa: E501


@pytest.mark.asyncio
async def test_command_youtubelist_cancel(monkeypatch):
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(youtube.Youtube(bot))
    dpytest.configure(bot)

    def mock_resp(*args, **kwargs):
        return [{'title': 'Pastime Paradise',
                 'type': 'video',
                 'id': '_H3Sv2zad6s'},
                {'title': "Gangsta's Paradise",
                 'type': 'video',
                 'id': 'fPO76Jlnz6c'}
                ]

    async def mock_pass(*args, **kwargs):
        msg = asynctest.Mock()
        msg.content = "cancel"
        msg.delete = asynctest.CoroutineMock()
        return msg

    monkeypatch.setattr(youtube, "search_youtube", mock_resp)
    monkeypatch.setattr(bot, "wait_for", mock_pass)

    await dpytest.message('!youtubelist 2 pastime paradise')
    res = dpytest.runner.sent_queue.get_nowait()

    # TODO: next line is ugly. We should use dpytest.verify_embed
    resp = res.embeds[0]._fields[0]['value']

    assert resp == '[Pastime Paradise](https://www.youtube.com/watch?v=_H3Sv2zad6s)'  # noqa: E501

    # Depop last object  ???
    # TODO: do something nicers
    dpytest.runner.sent_queue.get_nowait()


@pytest.mark.asyncio
async def test_command_youtubelist_not_cancel(monkeypatch):
    bot = commands.Bot(command_prefix='!')
    bot.add_cog(youtube.Youtube(bot))
    dpytest.configure(bot)

    def mock_resp(*args, **kwargs):
        return [{'title': 'Pastime Paradise',
                 'type': 'video',
                 'id': '_H3Sv2zad6s'},
                {'title': "Gangsta's Paradise",
                 'type': 'video',
                 'id': 'fPO76Jlnz6c'}
                ]

    async def mock_pass(*args, **kwargs):
        msg = asynctest.Mock()
        msg.content = 1
        msg.delete = asynctest.CoroutineMock()
        return msg

    monkeypatch.setattr(youtube, "search_youtube", mock_resp)
    monkeypatch.setattr(bot, "wait_for", mock_pass)

    await dpytest.message('!youtubelist 2 pastime paradise')
    # print("yata")
    res = dpytest.runner.sent_queue.get_nowait()
    # TODO: next line is ugly. We should use dpytest.verify_embed
    resp = res.embeds[0]._fields[0]['value']
    assert resp == '[Pastime Paradise](https://www.youtube.com/watch?v=_H3Sv2zad6s)'  # noqa: E501

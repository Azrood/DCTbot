import asyncio
import os
import glob

import pytest
import pytest_asyncio
import discord
import discord.ext.commands as commands
import discord.ext.test as dpytest
from discord.client import _LoopSentinel


@pytest_asyncio.fixture
async def bot(request, event_loop):
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    b = commands.Bot(command_prefix="!",
                     intents=intents)
    # set up the loop
    if isinstance(b.loop, _LoopSentinel):
        await b._async_setup_hook()

    dpytest.configure(b)
    return b


@pytest_asyncio.fixture(autouse=True)
async def cleanup():
    yield
    await dpytest.empty_queue()


@pytest.fixture
def mock_sleep(monkeypatch):
    """asyncio.sleep() mocked to return immediately."""

    async def return_now(*args, **kwargs):
        return

    monkeypatch.setattr(asyncio, "sleep", return_now)


def pytest_sessionfinish(session, exitstatus):
    """ Code to execute after all tests. """

    # dat files are created when using attachements, like cards from Card cog, etc...  # noqa: E501
    print("\n-------------------------\nClean dpytest_*.dat files")
    fileList = glob.glob('./dpytest_*.dat')
    for filePath in fileList:
        try:
            os.remove(filePath)
        except Exception:
            print("Error while deleting file : ", filePath)

    # Delete json log file created by the tests
    print("\n-------------------\nClean test log.json\n")
    log_test_file = "utils/test_log.json"
    try:
        os.remove(log_test_file)
    except FileNotFoundError:
        pass

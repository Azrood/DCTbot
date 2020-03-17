#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Unit tests."""

import aiohttp
import pytest
# from unittest.mock import MagicMock
import asynctest

from cogs.google import google_top_link, search_google


@pytest.mark.asyncio
async def test_google_top_link(monkeypatch):
    """Test google_top_link."""

    async def mock_resp(*args, **kwargs):
        txt = '''{"items": [
            {"kind": "customsearch#result", 
            "title": "Python Docs", 
            "link": "https://docs.python.org/"}
            ]}'''  # noqa

        # Let's create fake ("Mock") response, which text() always
        # returns txt string
        # See https://asynctest.readthedocs.io/en/latest/tutorial.mocking.html#mocking-of-coroutines  # noqa: E501
        mocked_resp = asynctest.Mock()
        mocked_resp.text = asynctest.CoroutineMock(return_value=txt)

        return mocked_resp

    monkeypatch.setattr(aiohttp.ClientSession, "get", mock_resp)

    # TODO:
    # I think we can do simpler than that, with a decorator (mock.patch ?)
    # to know more, please see :
    # https://docs.pytest.org/en/latest/monkeypatch.html
    # python doc

    res = await google_top_link("python doc")

    assert res['title'] == "Python Docs"
    assert res['url'] == "https://docs.python.org/"


@pytest.mark.asyncio
async def test_search_google(monkeypatch):
    """Test search_google()."""

    async def mock_resp(*args, **kwargs):
        txt = '''{"items": [
            {"kind": "customsearch#result", "title": "3.8.2rc2 Documentation", "link": "https://docs.python.org/"}, 
            {"kind": "customsearch#result", "title": "Documentation", "link": "https://www.python.org/doc/"}, 
            {"kind": "customsearch#result", "title": "Built-in Functions \u2014 Python 3.8.2rc2 documentation", "link": "https://docs.python.org/3/library/functions.html"}
            ]}'''  # noqa

        # Let's create fake ("Mock") response, which text() always
        # returns txt string
        # See https://asynctest.readthedocs.io/en/latest/tutorial.mocking.html#mocking-of-coroutines  # noqa: E501
        mocked_resp = asynctest.Mock()
        mocked_resp.text = asynctest.CoroutineMock(return_value=txt)

        return mocked_resp

    monkeypatch.setattr(aiohttp.ClientSession, "get", mock_resp)
    res = await search_google("python3 doc", 3)

    assert len(res) == 3
    assert res[0]["title"] == "3.8.2rc2 Documentation"

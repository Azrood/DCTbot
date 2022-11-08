#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Unit tests."""

import pytest

from cogs.getcomics import getcomics_top_link


@pytest.mark.asyncio
async def test_getcomics_top_link_title():
    """Test getcomics_top_link (title only)."""
    res = await getcomics_top_link("Batman Knightwatch #3")
    ref = "Batman – Knightwatch #3 (2022)"
    assert res[0] == ref

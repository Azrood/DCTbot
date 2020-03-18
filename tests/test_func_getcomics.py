#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Unit tests."""

import pytest

from cogs.getcomics import getcomics_top_link


@pytest.mark.asyncio
async def test_getcomics_top_link_title():
    """Test getcomics_top_link (title only)."""
    res = await getcomics_top_link("Batman #79")
    ref = "Batman #79 (2019)"
    assert res[0] == ref

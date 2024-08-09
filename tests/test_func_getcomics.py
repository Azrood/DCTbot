#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Unit tests."""

import pytest

from cogs.getcomics import getcomics_top_link


@pytest.mark.asyncio
async def test_getcomics_top_link_title():
    """Test getcomics_top_link (title only)."""
    res = await getcomics_top_link("New mutants vol 4")
    ref = "New Mutants Vol. 4 (TPB) (2023)"
    assert res[0] == ref

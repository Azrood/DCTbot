"""Unit tests."""

import pytest

from cogs.urban import UrbanSearch


@pytest.mark.asyncio
async def test_get_top_def():
    """Test UrbanSearch.get_top_def."""
    urban = UrbanSearch("Distro Hop")
    await urban.fetch()
    res = urban.get_top_def()
    ref = "Distro Hop"
    assert res[0] == ref

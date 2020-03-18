# import asyncio
# import datetime
import re
import pytest

from cogs import bonjourmadame


@pytest.mark.asyncio
async def test_latest_madame():
    """Test getcomics_top_link (title only)."""
    res = await bonjourmadame.latest_madame()
    assert re.match(r"https://i\d\.wp\.com/bonjourmadame\.fr/"
                    r"wp-content/uploads/\d{4}/.*?\.(jpg|png)", res)

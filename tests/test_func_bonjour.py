# import asyncio
# import datetime
import re
import pytest

from cogs import bonjourmadame


@pytest.mark.asyncio
async def test_latest_madame():
    """Test latest_madame() (this test makes a real online request)."""
    res = await bonjourmadame.latest_madame()
    assert re.match(r"https?://(?:i\d\.wp\.com/)?bonjourmadame\.fr/"
                    r"wp-content/uploads/\d{4}/.*?\.(?:jpg|jpeg|png|mp4)", res)

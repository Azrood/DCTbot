"""Module to get news on comicsblog.fr."""

from utils.tools import get_soup_html


async def get_comicsblog(numb):
    """Get latest news on comicsblog.fr.

    Args:
        numb (int): number of news to retrieve

    Returns:
        list: list of comicsblog news

    """
    num = int(numb)
    c_blog_rss = "http://www.comicsblog.fr/comicsblog.rss"

    soup = await get_soup_html(c_blog_rss)
    ls = soup.select('item')
    out = ls[:num]

    return out

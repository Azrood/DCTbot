from utils.tools import get_soup_html


def get_comicsblog(numb):
    num = int(numb)
    c_blog_rss = "http://www.comicsblog.fr/comicsblog.rss"

    soup = get_soup_html(c_blog_rss)
    ls = soup.select('item')
    out = ls[:num]

    return out

import requests
from bs4 import BeautifulSoup


def get_comicsblog(num):

    c_blog_rss = "http://www.comicsblog.fr/comicsblog.rss"

    res = requests.get(c_blog_rss)
    res.close()
    # BeautifulSoup will transform raw HTML in a tree easy to parse
    soup = BeautifulSoup(res.text, 'html.parser')
    ls = soup.select('item')
    out = ls[:num]

    return out
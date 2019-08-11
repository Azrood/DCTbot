# -*- coding: utf-8 -*-

# import os
import requests
import json
from urllib.parse import quote_plus
from utils.secret import token_youtube, DEVELOPER_CX


def search_google(user_input, number):

    google_search_url = "https://www.googleapis.com/customsearch/v1"

    params = {
        'q': quote_plus(user_input),
        'cx': DEVELOPER_CX,
        'safe': 'active',
        'hl': 'fr',
        'num': int(number),
        'fields': 'items(kind,link,title)',
        'key': token_youtube
    }

    response = requests.get(google_search_url, params=params)
    try:
        json_data = json.loads(response.text)["items"]
    except KeyError:
        json_data = []

    out = []

    for j in json_data:
        title = j['title']
        url = j['link']
        out.append({'title': title, 'url': url})

    return out


def google_top_link(user_input):
    try:
        result = search_google(user_input, number=1)
        return result[0]
    except IndexError:
        return None
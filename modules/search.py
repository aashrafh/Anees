from googleapiclient.discovery import build
from functools import reduce
from config import *


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


def search(text):
    result = google_search(text, MAP_API_KEY, CSE_ID)
    return get_results(result)


def parse_search_results(msg, item):
    return msg + f'\n\n<li><a href="{item[1]}">{item[0]}</a></li>'


def get_results(result):
    results = list()

    for item in result['items'][:5]:
        results.append([item['title'], item['link']])

    msg = '<ul>دي افضل نتايج لقيتها، اتمنى تفيدك:'
    msg = reduce(parse_search_results, results, msg) + "</ul>"
    return msg

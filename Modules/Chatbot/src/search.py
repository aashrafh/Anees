from googleapiclient.discovery import build
my_api_key = "AIzaSyDKR0mQtI6fh1bmcaMcdkWqGv0UuoZ7_uA"
my_cse_id = "32ccd6e123a6d49d7"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

def search(text):
    result = google_search(text, my_api_key, my_cse_id)
    return get_results(result)

def get_results(result):
    results = list()

    for item in result['items'][:5]:
        results.append([item['title'],item['link']])

    return results
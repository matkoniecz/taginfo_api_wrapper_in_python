import urllib
import urllib.request
import urllib.parse
import json

def values_of_key(key):
    page = 1
    while True:
        data = get_page_of_key_values(key, page)
        for entry in data:
            yield entry
        page += 1
        if len(data) < entries_per_page():
            break

def entries_per_page():
    return 999

def get_page_of_key_values(key, page):
    url = "https://taginfo.openstreetmap.org/api/4/key/values?key=" + urllib.parse.quote(key) + "&page=" + str(page) + "&rp=" + str(entries_per_page()) + "&sortname=count_all&sortorder=desc"
    return json_response_from_url(url)["data"]

def json_response_from_url(url):
    url = url.replace(" ", "%20")
    try:
        data = urllib.request.urlopen(url).read()
        return json.loads(data)
    except UnicodeEncodeError:
        print("failed to process", url)
        raise

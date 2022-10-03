import urllib
import urllib.request
import urllib.parse
import json
import datetime

def values_of_key(key):
    page = 1
    while True:
        data = get_page_of_key_values(key, page)
        for entry in data:
            yield entry["value"]
        page += 1
        if len(data) < entries_per_page():
            break

def values_of_key_with_data(key):
    page = 1
    while True:
        data = get_page_of_key_values(key, page)
        for entry in data:
            yield entry
        page += 1
        if len(data) < entries_per_page():
            break

def tagging_used_by_project(project):
    page = 1
    while True:
        data = get_page_of_tags_used_by_project(project, page)
        for entry in data:
            yield entry
        page += 1
        if len(data) < entries_per_page():
            break

def entries_per_page():
    return 999

def throw_exception_on_suspicious_page_index(page):
    if page == 0:
        raise ValueError("see https://taginfo.openstreetmap.org/taginfo/apidoc - pages are starting from 1, page=0 will (I think) disable paging and list all values") # TODO: investigate
    # TODO - test also negative, nonnumeric?

def get_url_for_all_keys(page, extra_query_part=""):
    throw_exception_on_suspicious_page_index(page)
    # https://taginfo.openstreetmap.org/api/4/keys/all?page=1&rp=100&sortname=count_all&sortorder=desc
    return "https://taginfo.openstreetmap.org/api/4/keys/all?page=" + str(page) + "&rp=" + str(entries_per_page()) + "&sortname=count_all&sortorder=desc" + extra_query_part

def get_page_of_all_keys(page):
    # https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_keys_all
    return json_response_from_url(get_url_for_all_keys(page))["data"]

def get_page_of_all_keys_with_wiki_page(page):
    # https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_keys_all
    # https://taginfo.openstreetmap.org/api/4/keys/all?page=1&rp=100&sortname=count_all&sortorder=desc&filter=in_wiki
    return json_response_from_url(get_url_for_all_keys(page, "&filter=in_wiki"))["data"]

def get_page_of_key_values(key, page):
    throw_exception_on_suspicious_page_index(page)
    # https://taginfo.openstreetmap.org/api/4/key/values?key=surface&sortorder=desc
    url = "https://taginfo.openstreetmap.org/api/4/key/values?key=" + urllib.parse.quote(key) + "&page=" + str(page) + "&rp=" + str(entries_per_page()) + "&sortname=count_all&sortorder=desc"
    return json_response_from_url(url)["data"]

def get_page_of_tags_used_by_project(project, page):
    throw_exception_on_suspicious_page_index(page)
    url = "https://taginfo.openstreetmap.org/api/4/project/tags?project=" + project + "&page=" + str(page) + "&rp=" + str(entries_per_page()) + "&sortname=tag&sortorder=asc"
    return json_response_from_url(url)["data"]

def count_appearances_of_tag(key, value):
    # https://taginfo.openstreetmap.org/api/4/tag/stats?key=building&value=yes
    url = "https://taginfo.openstreetmap.org/api/4/tag/stats?key=" + urllib.parse.quote(key) + "&value=" + urllib.parse.quote(value)
    data = json_response_from_url(url)
    return data['data'][0]['count']

def count_appearances_of_key(key):
    # https://taginfo.openstreetmap.org/api/4/tag/stats?key=building
    url = "https://taginfo.openstreetmap.org/api/4/key/stats?key=" + urllib.parse.quote(key)
    data = json_response_from_url(url)
    return data['data'][0]['count']

def get_all_raw_data_about_key_use(key):
    url = "https://taginfo.openstreetmap.org/api/4/key/chronology?key=" + urllib.parse.quote(key)
    data = json_response_from_url(url)
    return data['data']

def get_all_raw_data_about_tag_use(key, value):
    # https://taginfo.openstreetmap.org/tags/?key=type&value=associated_address#chronology
    # https://taginfo.openstreetmap.org/api/4/tag/chronology?key=type&value=associated_address
    # https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_tag_chronology
    url = "https://taginfo.openstreetmap.org/api/4/tag/chronology?key=" + urllib.parse.quote(key) + "&value=" + urllib.parse.quote(value)
    data = json_response_from_url(url)
    return data['data']

def count_new_appearances_of_tag_historic_data_from_deltas(data, days_ago):
    initial_day = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    if data == []:
        return None
    diff = 0
    for offset in range(1, days_ago):
        if len(data) < offset:
            break
        taginfo_format = '%Y-%m-%d'
        datetime_of_datapoint = datetime.datetime.strptime(data[-offset]["date"], taginfo_format)
        if(datetime_of_datapoint < initial_day):
            # gaps are possiple in cases where tag does not changed value
            # https://taginfo.openstreetmap.org/tags/?key=type&value=associated_address#chronology
            # https://taginfo.openstreetmap.org/api/4/tag/chronology?key=type&value=associated_address
            break
        diff += data[-offset]["nodes"]
        diff += data[-offset]["ways"]
        diff += data[-offset]["relations"]
    return diff

def count_new_appearances_of_tag_historic_data(key, value, days_ago):
    data = get_all_raw_data_about_tag_use(key, value)
    return count_new_appearances_of_tag_historic_data_from_deltas(data, days_ago)

def count_new_appearances_of_key_historic_data(key, days_ago):
    data = get_all_raw_data_about_key_use(key)
    return count_new_appearances_of_tag_historic_data_from_deltas(data, days_ago)

def json_response_from_url(url):
    url = url.replace(" ", "%20")
    try:
        data = urllib.request.urlopen(url).read()
        return json.loads(data)
    except UnicodeEncodeError:
        print("failed to process", url)
        raise
    except urllib.error.URLError as e:
        print(url)
        print(url)
        if "connection timed out"  in str(e):
            return json_response_from_url(url)
        else:
            raise

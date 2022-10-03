# Taginfo

This project exists to access magnificent [taginfo](https://taginfo.openstreetmap.org/) maintained by Jochen Topf.

It is an unofficial Python wrapper over available API.

It is a Python wrapper for a tiny part of [taginfo API](https://taginfo.openstreetmap.org/taginfo/apidoc) that I use in my projects.

Note that the taginfo API is intended for the use of the OpenStreetMap community. Do not use it for other purposes. ([source](https://wiki.openstreetmap.org/wiki/Taginfo/API)) As taginfo is open source you can deploy own service of needed.

# Examples
<!-- in case of editing or adding samples here, change also tests -->

## How often given key is used?

```
import taginfo

key = "name:ab"
print(key, "is used", taginfo.query.count_appearances_of_key(key), "times")
```

## Listing popular values for key

```
import taginfo

key = "bin"
print("all values of specific key:")
for value in taginfo.query.values_of_key(key):
    print(key, "=", value)
print()
key = "surface"
print("all popular values of specific key:")
for entry in taginfo.query.values_of_key_with_data(key):
    if(entry['count'] > 1000):
        print(key, "=", entry['value'], str(int(entry['count']/1000)) + "k")
```

## Listing popular tags unsupported by iD

See https://github.com/openstreetmap/id-tagging-schema/issues/529 - this is actually used by iD project

```
import taginfo

def show_popular_tags_not_supported_by_project(project, key, excluded_values, threshold):
    expected_support = []
    cached_value_info = {}
    for entry in taginfo.query.values_of_key_with_data(key):
        if(entry['count'] > threshold):
            expected_support.append(entry["value"])
            cached_value_info[entry["value"]] = entry
    for entry in taginfo.query.tagging_used_by_project(project):
        if entry["key"] == key:
            if(entry["value"] != None):
                if entry["value"] in expected_support:
                    expected_support.remove(entry["value"])

    for entry in expected_support:
        if entry not in excluded_values:
            link = "https://taginfo.openstreetmap.org/tags/" + key + "=" + entry
            text = "`" + key + " = " + cached_value_info[entry]['value'] + "` " + str(int(cached_value_info[entry]['count']/1000)) + "k"
            linked_markdown_text = "* [ ] [" + text + "](" + link + ")"
            print(linked_markdown_text)

project = "id_editor"
# keys based on https://wiki.openstreetmap.org/wiki/Map_features
show_popular_tags_not_supported_by_project(project, "surface", [], 1_000)
show_popular_tags_not_supported_by_project(project, "building", ["yes"], 100_000)
show_popular_tags_not_supported_by_project(project, "shop", ["yes", "no"], 1_000)
show_popular_tags_not_supported_by_project(project, "craft", ["yes"
    "grinding_mill", # import only https://taginfo.openstreetmap.org/tags/craft=grinding_mill#chronology
], 1_000)
show_popular_tags_not_supported_by_project(project, "natural", [
    "crevasse" # inflated by imports, see https://taginfo.openstreetmap.org/tags/natural=crevasse#chronology
    ], 10_000)
show_popular_tags_not_supported_by_project(project, "leisure", [], 5_000)
show_popular_tags_not_supported_by_project(project, "amenity", [], 5_000)
show_popular_tags_not_supported_by_project(project, "landuse", [], 20_000)
show_popular_tags_not_supported_by_project(project, "power", [
    "abandoned:tower" # it clearly should be abandoned:power=tower
], 2_000)
show_popular_tags_not_supported_by_project(project, "place", [], 10_000)
show_popular_tags_not_supported_by_project(project, "railway", ["razed", "proposed"], 5_000)
show_popular_tags_not_supported_by_project(project, "barrier", [], 3_000)
show_popular_tags_not_supported_by_project(project, "highway", ["proposed", "no"], 1_000)
show_popular_tags_not_supported_by_project(project, "tourism", ["yes"], 1_000)
show_popular_tags_not_supported_by_project(project, "waterway", ["artificial"], 5_000)
show_popular_tags_not_supported_by_project(project, "man_made", [
    "advertising", # nowadays advertising is added without that
], 3_000)
show_popular_tags_not_supported_by_project(project, "advertising", [], 3_000)
show_popular_tags_not_supported_by_project(project, "aerialway", [], 1_000)
show_popular_tags_not_supported_by_project(project, "aeroway", [], 1_000)
show_popular_tags_not_supported_by_project(project, "boundary", [], 15_000)
show_popular_tags_not_supported_by_project(project, "emergency", [], 1_000)
show_popular_tags_not_supported_by_project(project, "cycleway", [], 5_000)
show_popular_tags_not_supported_by_project(project, "cycleway:left", [], 5_000)
show_popular_tags_not_supported_by_project(project, "cycleway:right", [], 5_000)
show_popular_tags_not_supported_by_project(project, "cycleway:both", [], 5_000)
show_popular_tags_not_supported_by_project(project, "historic", [], 10_000)
show_popular_tags_not_supported_by_project(project, "military", [], 2_000)
show_popular_tags_not_supported_by_project(project, "office", [
    "logistics" # debris left by User:RTFM
], 2_000)
show_popular_tags_not_supported_by_project(project, "route", [], 2_000)
show_popular_tags_not_supported_by_project(project, "sport", [
    "cricket_nets", # not an actual sport
], 2_500)
show_popular_tags_not_supported_by_project(project, "healthcare", ["hospital", "pharmacy", "doctor", "clinic", "dentist"], 1_000)
```

## Listing popular keys not supported by iD

```
# no issue created for it at https://github.com/openstreetmap/id-tagging-schema/issues
# right now it provides no useful info (more ntries need to be skipped or verified)
project = "id_editor"
supported = []
threshold = 500_000
expected_support = []
for entry in taginfo.query.tagging_used_by_project(project):
    if entry["key"] not in supported:
        supported.append(entry["key"]) # will not catch cases where only specific value is supported
page = 1
finished = False
while not finished:
    for entry in taginfo.query.get_page_of_all_keys_with_wiki_page(page):
        if(entry['count_all'] < threshold):
            finished = True
            break
        key = entry["key"]
        banned_key_prefix_indicating_import_garbage = ["tiger:", "nhd:", "NHD:", "lacounty:", "ref:", "nysgissam:", "nycdoitt:", "yh:", "building:ruian:", "gnis:", "osak:", "maaamet:", "chicago:"]
        matches_blacklisted = False
        for prefix in banned_key_prefix_indicating_import_garbage:
            if key.find(prefix) == 0:
                matches_blacklisted = True
                break
        if matches_blacklisted:
            continue
        if key in ["created_by"]: # deprecated/discardable, not listed in iD taginfo project
            continue
        if key not in supported:
            formatted_count = str(int(entry["count_all"]/1000))+"k"
            print(key, formatted_count)
            expected_support.append({"key": key, "count": formatted_count})
    page += 1

for entry in expected_support:
    link = "https://taginfo.openstreetmap.org/keys/" + entry["key"]
    text = "`" + entry["key"] + "` " + entry["count"]
    linked_markdown_text = "[" + text + "](" + link + ")"
    print(linked_markdown_text)
```
## Historic data

```
import taginfo

print("Intended to show useful info (and maybe motivate you to talk to this mappers and ask whether they meant surface=concrete:")
print(taginfo.query.count_new_appearances_of_tag_historic_data("surface", "cement", 60), "net change for surface=cement within last 60 days (this tag appears to be duplicating surface=concrete)")
print()
print("intended to show that such short-term queries are likely to be a problem, as taginfo may have delay in updating and last few days may be often unavailable:")
print(taginfo.query.count_new_appearances_of_key_historic_data("building", 1), "new building=* objects since yesterday")
```

# Development

Contributions are welcome to cover larger part of taginfo API.

## Run tests

`python3 -m unittest`
# Taginfo

This project exists to access magnificent [taginfo](https://taginfo.openstreetmap.org/) maintained by Jochen Topf.

It is an unofficial Python wrapper over available API.

It is a Python wrapper for a tiny part of [taginfo API](https://taginfo.openstreetmap.org/taginfo/apidoc) that I use in my projects.

Note that the taginfo API is intended for the use of the OpenStreetMap community. Do not use it for other purposes. ([source](https://wiki.openstreetmap.org/wiki/Taginfo/API)) As taginfo is open source you can deploy own service of needed.

# Installation

Like any other python package: `pip install taginfo`

# Examples
<!-- in case of editing or adding samples here, change also tests -->

## How often given key is used?

```
import taginfo

key = "name:ab"
print(key, "is used", taginfo.query.count_appearances_of_key(key), "times")
```

## What about tags?

```
import taginfo

key = "horse"
value = "noo"
print(key, "=", value, "is used", taginfo.query.count_appearances_of_tag(key, value), "times")
value = "no"
print(key, "=", value, "is used", taginfo.query.count_appearances_of_tag(key, value), "times")
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

See [https://github.com/openstreetmap/id-tagging-schema/issues/1641](https://github.com/openstreetmap/id-tagging-schema/issues/1641) for output

See `test_tags_used_in_project` in [tests.py](tests.py) for code used to generate it.

## Listing popular keys not supported by iD

```
# no issue created for it at https://github.com/openstreetmap/id-tagging-schema/issues
# right now it provides no useful info (more entries need to be skipped or verified)
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
        banned_key_prefix_indicating_import_garbage = ["tiger:", "nhd:", "NHD:", "lacounty:", "ref:", "nysgissam:", "nycdoitt:", "yh:", "building:ruian:", "gnis:", "osak:", "maaamet:", "chicago:", "LINZ:"]
        matches_blacklisted = False
        for prefix in banned_key_prefix_indicating_import_garbage:
            if key.find(prefix) == 0:
                matches_blacklisted = True
                break
        if matches_blacklisted:
            continue
        if key in [
            "created_by", # deprecated/discardable, not listed in iD taginfo project
            "is_in", # deprecated and unwanted
            "name_1", # weird tagging promoted by old iD versions
            "addr:TW:dataset", # unwanted import tag
        ]:
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
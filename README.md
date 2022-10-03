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

key = "surface"
for value in taginfo.query.values_of_key(key):
    print(key, "=", value)
print()
for entry in taginfo.query.values_of_key_with_data(key):
    if(entry['count'] > 1000):
        print(key, "=", entry['value'], str(int(entry['count']/1000)) + "k")
```

## Listing popular tags unsupported by iD

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
            text = key + " = " + cached_value_info[entry]['value'] + " " + str(int(cached_value_info[entry]['count']/1000)) + "k"
            linked_markdown_text = "[" + text + "](" + link + ")"
            print(linked_markdown_text)

project = "id_editor"
show_popular_tags_not_supported_by_project(project, "surface", [], 1_000)
show_popular_tags_not_supported_by_project(project, "building", ["yes"], 100_000)
show_popular_tags_not_supported_by_project(project, "shop", ["yes", "no"], 1_000)
show_popular_tags_not_supported_by_project(project, "natural", [], 10_000)
show_popular_tags_not_supported_by_project(project, "leisure", [], 5_000)
show_popular_tags_not_supported_by_project(project, "amenity", [], 5_000)
show_popular_tags_not_supported_by_project(project, "landuse", [], 20_000)
show_popular_tags_not_supported_by_project(project, "power", [], 2_000)
show_popular_tags_not_supported_by_project(project, "place", [], 10_000)
show_popular_tags_not_supported_by_project(project, "railway", ["razed", "proposed"], 5_000)
show_popular_tags_not_supported_by_project(project, "barrier", [], 3_000)
show_popular_tags_not_supported_by_project(project, "highway", ["proposed", "no"], 1_000)
show_popular_tags_not_supported_by_project(project, "tourism", ["yes"], 1_000)
show_popular_tags_not_supported_by_project(project, "waterway", ["artificial"], 5_000)
```

# Development

Contributions are welcome to cover larger part of taginfo API.

## Run tests

`python3 -m unittest`
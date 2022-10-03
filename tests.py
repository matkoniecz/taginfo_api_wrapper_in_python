import unittest
import taginfo

class Tests(unittest.TestCase):
    def test_run_readme_code_key_usage_count(self):
        key = "name:ab"
        print(key, "is used", taginfo.query.count_appearances_of_key(key), "times")

    def test_run_readme_code_values_of_key(self):
        key = "surface"
        for value in taginfo.query.values_of_key(key):
            print(key, "=", value)        
        print()
        for entry in taginfo.query.values_of_key_with_data(key):
            if(entry['count'] > 1000):
                print(key, "=", entry['value'], str(int(entry['count']/1000)) + "k")

    def test_run_readme_code_tags_used_in_project(self):
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

    def test_run_readme_popularity(self):
        print("Intended to show useful info (and maybe motivate you to talk to this mappers and ask whether they meant surface=concrete:")
        print(taginfo.query.count_new_appearances_of_tag_historic_data("surface", "cement", 60), "net change for surface=cement within last 60 days (this tag appears to be duplicating surface=concrete)")
        print()
        print("intended to show that such short-term queries are likely to be a problem, as taginfo may have delay in updating and last few days may be often unavailable:")
        print(taginfo.query.count_new_appearances_of_key_historic_data("building", 1), "new building=* objects since yesterday")

    def test_basic_math(self):
        self.assertEqual(2-2, 0)

if __name__ == '__main__':
    unittest.main()

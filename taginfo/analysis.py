import taginfo.query


def get_tagging_supported_by_id_except_deprecations():
    def is_undeprecated_id_entry(entry):
        return is_entry_implying_deprecation_by_id(entry) == False
    return get_tagging_used_by_project("id_editor", is_undeprecated_id_entry)

def get_tagging_deprecated_by_id():
    def is_deprecated_id_entry(entry):
        return is_entry_implying_deprecation_by_id(entry) == True
    return get_tagging_used_by_project("id_editor", is_deprecated_id_entry)

def is_entry_implying_deprecation_by_id(entry):
    if 'description' not in entry:
        return False
    if entry['description'] == None:
        # see say
        # {'key': 'plant:method', 'value': 'thermal', 'on_node': True, 'on_way': True, 'on_relation': True, 'on_area': True, 'description': None, 'doc_url': None, 'icon_url': None, 'count_all': 201, 'in_wiki': True}
        return False
    return "🄳 (deprecated tag) ➜" in entry['description']

def get_tagging_used_by_nsi():
    return get_tagging_used_by_project('name_suggestion_index')

def get_tagging_used_by_project(project, filter_function = None):
    project_tagging = {}
    for entry in taginfo.query.tagging_used_by_project(project):
        key = entry["key"]
        value = entry["value"]
        if filter_function == None or filter_function(entry):
            if(value != None):
                if key not in project_tagging:
                    project_tagging[key] = {}
                project_tagging[key][value] = entry
    return project_tagging

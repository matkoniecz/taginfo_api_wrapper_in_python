import taginfo.query

def get_tagging_supported_by_id_except_deprecations():
    project = "id_editor"
    project_tagging = {}
    for entry in taginfo.query.tagging_used_by_project(project):
        key = entry["key"]
        value = entry["value"]
        if entry["description"] != None:
            if "🄳 (deprecated tag) ➜" in entry["description"]:
                continue
        if(value != None):
            if key not in project_tagging:
                project_tagging[key] = {}
            project_tagging[key][value] = entry
    return project_tagging

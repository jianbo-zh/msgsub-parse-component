import json
import jsonpath
from ..textanalyse import extract_tags

def handler(jsonstr, tasks):
    try:
        jsonobj = json.loads(jsonstr)
    except json.JSONDecodeError as e:
        raise e

    datas = []
    for task in tasks:
        contents = []
        items = jsonpath.jsonpath(jsonobj, task)
        if hasattr(items, '__iter__'):
            for item in items:
                tags = extract_tags(item)
                contents.append({
                    "content": item,
                    "tags" : tags
                })

        datas.append({
            'task' : task,
            'contents' : contents
        })
    
    return datas

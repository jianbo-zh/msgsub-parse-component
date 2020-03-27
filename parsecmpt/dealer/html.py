from pyquery import PyQuery as pq
from ..textanalyse import extract_tags

def handler(htmlstr, tasks):
    datas = []
    pqobj = pq(htmlstr)
    for task in tasks:
        contents = []
        items = pqobj(task)
        if hasattr(items, '__iter__'):
            for item in items:
                tags = extract_tags(item.text)
                contents.append({
                    "content": item.text,
                    "tags" : tags
                })

        datas.append({
            'task' : task,
            'contents' : contents
        })

    return datas

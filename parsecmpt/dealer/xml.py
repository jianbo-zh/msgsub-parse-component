from lxml import etree
from ..textanalyse import extract_tags

def handler(xmlstr, tasks):
    
    xmlobj = etree.fromstring(bytes(xmlstr, encoding="utf-8"))

    datas = []
    for task in tasks:
        contents = []
        items = xmlobj.xpath(task)
        if hasattr(items, '__iter__'):
            for item in items:
                txt = item.text if hasattr(item, 'text') else item
                tags = extract_tags(txt)
                contents.append({
                    "content": txt,
                    "tags" : tags
                })

        datas.append({
            'task' : task,
            'contents' : contents
        })
    
    return datas
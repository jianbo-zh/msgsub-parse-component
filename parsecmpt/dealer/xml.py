from lxml import etree

def handler(xmlstr, tasks):
    
    xmlobj = etree.fromstring(bytes(xmlstr, encoding="utf-8"))

    datas = []
    for task in tasks:
        contents = []
        items = xmlobj.xpath(task)
        if hasattr(items, '__iter__'):
            for item in items:
                txt = item.text if hasattr(item, 'text') else item
                contents.append(txt)

        datas.append({
            'task' : task,
            'contents' : contents
        })
    
    return datas
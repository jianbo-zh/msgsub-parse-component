from lxml import etree

def handler(xmlstr, tasks):
    
    xmlobj = etree.XML(xmlstr)

    datas = []
    for task in tasks:
        contents = []
        items = xmlobj.xpath(task)
        for item in items:
            txt = item.text if hasattr(item, 'text') else item
            contents.append(txt)

        datas.append({
            'task' : task,
            'contents' : contents
        })
    
    return datas
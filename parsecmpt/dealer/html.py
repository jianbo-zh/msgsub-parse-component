from pyquery import PyQuery as pq

def handler(htmlstr, tasks):
    datas = []
    pqobj = pq(htmlstr)
    for task in tasks:
        contents = []
        items = pqobj(task)
        if hasattr(items, '__iter__'):
            for item in items:
                contents.append(item.text)

        datas.append({
            'task' : task,
            'contents' : contents
        })

    return datas

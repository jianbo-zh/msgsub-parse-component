from pyquery import PyQuery as pq

def handler(htmlstr, tasks):
    datas = []
    pqobj = pq(htmlstr)
    for task in tasks:
        contents = []
        items = pqobj(task)
        for item in items:
            contents.append(item.text)

        datas.append({
            'task' : task,
            'contents' : contents
        })

    return datas

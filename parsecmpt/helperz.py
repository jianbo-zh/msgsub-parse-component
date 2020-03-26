from . import constz

def get_content_type(ctstr):
    '''
    获取内容类型、字符集
    '''
    li = ctstr.lower().split(";", 2)

    if len(li) == 0:
        raise ValueError('unkown content type: [%s]' % ctstr)

    content_type = li[0].strip()

    if content_type not in [constz.CT_HTML, constz.CT_XML, constz.CT_JSON]:
        raise ValueError('unsupport content type: [%s]' % content_type)

    return content_type
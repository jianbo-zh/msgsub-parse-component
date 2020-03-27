import os
import logging
import jieba
import jieba.analyse as janalyse

_dictdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "userdict"))

_udfilepath = os.path.join(_dictdir, "user_words.txt")
_swfilepath = os.path.join(_dictdir, "stop_words.txt")

if not os.path.isfile(_udfilepath) or not os.path.isfile(_swfilepath):
    raise ImportError("no user_words.txt or stop_words.txt file")

_allowpos = ("n", "ns", "nt", "nz", "nrfg", "vn", "v")

# 关闭jieba调试信息
jieba.setLogLevel(logging.INFO)
jieba.initialize()
jieba.load_userdict(_udfilepath)
jieba.analyse.set_stop_words(_swfilepath)


def extract_tags(cntstr, word_count=100):
    """
    获取文本字符串中的关键词
    """

    words = jieba.analyse.textrank(
        cntstr, topK=word_count, withWeight=False, allowPOS=_allowpos, withFlag=False
    )

    return words

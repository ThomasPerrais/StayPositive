from elasticsearch import Elasticsearch
from datetime import date, timedelta
from typing import List

_INDEX = "moments"
es = Elasticsearch([{'host': 'elasticsearch', 'port':9200, 'scheme':'http'}])


def store(moments: List[str], gap: int = 0, index: str = _INDEX):
    actions = []
    for m in moments:
        action = {"index": {"_index": index}}
        doc = {
            "text": m,
            "date": date.today() - timedelta(gap),
            }
        actions.append(action)
        actions.append(doc)
    try:
        res = es.bulk(index=index, operations=actions)
        return not res["errors"]
    except:
        return False

def __get_query(gap: int):
    """
    Get the Elasticsearch query to retrieve moments whose date is given by the *gap* (in days) with today
    """
    if gap:
        gte = "now-{}d/d".format(str(gap))
        lt = "now-{}d/d".format(str(gap - 1))
        body = {"query": {"range": {"date": {"gte": gte, "lt": lt}}}}
    else:
        body = {"query": {"range": {"date": {"gte": "now/d"}}}}
    return body


def exist_for_date(gap: int = 0, index: str = _INDEX):
    if gap > 0:
        # moments for days to come do not exist
        return False
    body = __get_query(-gap)
    res = es.count(index=index, body=body)["count"]
    return res > 0


def get_for_date(gap: int = 0, index: str = _INDEX):
    body = __get_query(-gap)
    hits = es.search(index=index, body=body)["hits"]["hits"]
    return [hit["_source"]["text"] for hit in hits]

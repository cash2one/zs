from elasticsearch import Elasticsearch


es = Elasticsearch("http://dev.tax.elasticsearch.zs")

while True:
    res = es.search(index="arbitrations",
                    body={"fields": ["_id"], "query": {"match": {"doc_source_province":"浙江"}}})
    for re in res.get('hits').get('hits'):
        print(re.get('_id'))
        es.delete(index="arbitrations", doc_type="spider", id=re.get('_id'),  ignore=[400, 404])

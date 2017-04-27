from elasticsearch import Elasticsearch
import elasticsearch.helpers
from . import Environmental_parameters
import logging
import pyes

es_logger = logging.getLogger('elasticsearch')
es_logger.setLevel(logging.ERROR)

es = Elasticsearch(Environmental_parameters.es_url)

def add_mapping():
    try:
        conn = pyes.ES(Environmental_parameters.es_url)
        conn.indices.create_index(Environmental_parameters.es_index)
        mapping = {
          "doc_abstract": {
            "type": "string"
          },
          "doc_content": {
            "type": "string"
          },
          "doc_source": {
            "type": "string"
          },
          "doc_spider_name": {
            "type": "string"
          },
          "doc_time": {
            "type": "date",
            "format": "strict_date_optional_time||epoch_millis"
          },
          "doc_title": {
            "type": "string"
          },
          "doc_type": {
            "type": "string"
          },
          "doc_url": {
            "type": "string"
          }
        }

        conn.indices.put_mapping(Environmental_parameters.es_type, {'properties': mapping}, [Environmental_parameters.es_index])
    except Exception as e:
        print(e)


def es_save(json_data):
    actions = [
        {
            '_op_type': 'index',
            '_index': Environmental_parameters.es_index,
            '_type': Environmental_parameters.es_type,
            '_source': {
                "doc_type": d.get("type", ""),
                "doc_spider_name": d.get("spider_name", ""),
                "doc_url": d.get("url", ""),
                "doc_title": d.get("title", ""),
                "doc_time": d.get("time", ""),
                "doc_content": d.get("content", ""),
                "doc_abstract": d.get("abstract", ""),
                "doc_source": d.get("source", ""),
            }
        }
        for d in json_data
    ]
    try:
        elasticsearch.helpers.bulk(es, actions)
    except Exception as e:
        print(e)



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
          "doc_source_city": {
            "type": "string"
          },
          "doc_source_province": {
            "type": "string"
          },
          "doc_tribunal_applicant": {
            "type": "string"
          },
          "doc_tribunal_arbitrator": {
            "type": "string"
          },
          "doc_tribunal_clerk": {
            "type": "string"
          },
          "doc_tribunal_commission_name": {
            "type": "string"
          },
          "doc_tribunal_place": {
            "type": "string"
          },
          "doc_tribunal_reason": {
            "type": "string"
          },
          "doc_tribunal_time": {
            "type": "date",
            "format": "strict_date_optional_time||epoch_millis"
          },
          "doc_tribunal_title": {
            "type": "string"
          },
          "doc_tribunal_units": {
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
                "doc_url": d.get("url", ""),
                "doc_tribunal_title": d.get("tribunal_title", ""),
                "doc_tribunal_units": d.get("tribunal_units", ""),
                "doc_tribunal_commission_name": d.get("tribunal_commission_name", ""),
                "doc_tribunal_time": d.get("tribunal_time", ""),
                "doc_tribunal_applicant": d.get("tribunal_applicant", ""),
                "doc_tribunal_place": d.get("tribunal_place", ""),
                "doc_source_city": d.get("source_city", ""),
                "doc_source_province": d.get("source_province", ""),
                "doc_tribunal_reason": d.get("tribunal_reason", ""),
                "doc_tribunal_arbitrator": d.get("tribunal_arbitrator", ""),
                "doc_tribunal_clerk": d.get("tribunal_clerk", ""),
            }
        }
        for d in json_data
    ]
    try:
        elasticsearch.helpers.bulk(es, actions)
    except Exception as e:
        print(e)



# from elasticsearch import Elasticsearch
# import elasticsearch.helpers
# from . import Environmental_parameters
# import logging
# import pyes
#
# es_logger = logging.getLogger('elasticsearch')
# es_logger.setLevel(logging.ERROR)
#
# es = Elasticsearch(Environmental_parameters.es_url)
#
# def add_mapping():
#     try:
#         conn = pyes.ES(Environmental_parameters.es_url)
#         conn.indices.create_index(Environmental_parameters.es_index)
#         mapping = {
#           "doc_arbitration_commission_name": {
#             "type": "string"
#           },
#           "doc_arbitration_person": {
#             "type": "string"
#           },
#           "doc_arbitration_title": {
#             "type": "string"
#           },
#           "doc_arbitration_units": {
#             "type": "string"
#           },
#           "doc_content": {
#             "type": "string"
#           },
#           "doc_divison_code": {
#             "type": "string"
#           },
#           "doc_source_city": {
#             "type": "string"
#           },
#           "doc_source_province": {
#             "type": "string"
#           },
#           "doc_time": {
#             "type": "date",
#             "format": "strict_date_optional_time||epoch_millis"
#           },
#           "doc_url": {
#             "type": "string"
#           }
#         }
#
#         conn.indices.put_mapping(Environmental_parameters.es_type, {'properties': mapping}, [Environmental_parameters.es_index])
#     except Exception as e:
#         print(e)
#
#
# def es_save(json_data):
#     actions = [
#         {
#             '_op_type': 'index',
#             '_index': Environmental_parameters.es_index,
#             '_type': Environmental_parameters.es_type,
#             '_source': {
#                 "doc_url": d.get("url", ""),
#                 "doc_arbitration_title": d.get("Arbitration_title", ""),
#                 'doc_arbitration_units': d.get("Arbitration_units", ""),
#                 "doc_arbitration_commission_name": d.get("Arbitration_commission_name", ""),
#                 "doc_time": d.get("time", ""),
#                 "doc_content": d.get("content", ""),
#                 "doc_arbitration_person": d.get("Arbitration_person", ""),
#                 "doc_source_city": d.get("source_city", ""),
#                 "doc_source_province": d.get("source_province", ""),
#                 "doc_divison_code": d.get("divison_code", ""),
#             }
#         }
#         for d in json_data
#     ]
#     try:
#         elasticsearch.helpers.bulk(es, actions)
#     except Exception as e:
#         print(e)
#
#

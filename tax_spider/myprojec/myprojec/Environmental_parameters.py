import os

es_url = os.environ.get("ES_URL", "http://dev.tax.elasticsearch.zs:80")
es_index = os.environ.get("ES_INDEX", "informations")
es_type = os.environ.get("ES_TYPE", "spider")
redis_host = os.environ.get("REDIS_HOST", "192.168.5.220")
redis_port = os.environ.get("REDIS_PORT", 6379)
log_path = os.environ.get("LOG_PATH", "")
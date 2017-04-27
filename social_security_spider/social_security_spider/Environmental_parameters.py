import os

mongodb_server = os.environ.get("MONGODB_SERVER", "192.168.1.220")
mongodb_port = os.environ.get("MONGODB_PORT", 27017)
mongodb_db = os.environ.get("MONGODB_DB", "social_security")
log_path = os.environ.get("LOG_PATH", "")

import os

KAFKA_CONFIG = {'bootstrap_servers': os.environ.get("KAFKA_URL")}

# from elasticsearch import Elasticsearch
#
# es = Elasticsearch("http://localhost:9200")
from elasticsearch import Elasticsearch

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    http_auth=("elastic", "changeme"),  # אם נדרש אימות
    verify_certs=False  # אם יש בעיות עם אימות תעודות

)
print("yessss")

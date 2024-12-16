from elasticsearch import Elasticsearch

# es = Elasticsearch("http://localhost:9200")
# from elasticsearch import Elasticsearch

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    http_auth=("elastic", "changeme"),  # אם נדרש אימות
    timeout=30  # הגדל זמן התגובה אם החיבור איטי
)

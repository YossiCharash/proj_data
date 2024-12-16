
from database.elasticsearch.config import es






def insert_data(data,index_name = "reviews"):
    mapping = {
        "mappings": {
            "properties": {
                "uuid": {"type": "keyword"},
                "name": {"type": "text"},
                "metric": {"type": "integer"},
                "index": {"type": "integer"},
                "ip": {"type": "ip"},
                "date": {
                    "type": "date",
                    "format": "dd-MM-yyyy HH:mm"
                },
                "additional_ip": {"type": "ip"},
                "id": {"type": "integer"}
            }
        }
    }


    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mapping)
        print(f"Index '{index_name}' created with mapping.")
    else:
        print(f"Index '{index_name}' already exists.")

        result = {
            "review_id": data[0],
            "content": data[1],
            "score": data[2],
            "thumbs_up_count": data[3],
            "review_created_version": data[4],
            "date_time": data[5],
            "app_version": data[6],
            "student_id": data[7]
        }

        res = es.index(index=index_name, body=result)
        print(f"Document added with ID: {res['_id']}")

# הרצת הסקריפט
if __name__ == "__main__":
    insert_data()
import csv
import json
from confluent_kafka import Producer
from kafka.config_kafka import KAFKA_BROKER



producer = Producer({'bootstrap.servers': KAFKA_BROKER})



def send_to_kafka(topic, data):
    producer.produce(topic, value=json.dumps(data).encode('utf-8'))
    producer.flush()
    print(f"Sent message to Kafka: {data}")


def read_csv(topic,path):
    with open(path, 'r') as f:
        data = csv.reader(f)
        for row in data:
            print(row)
            send_to_kafka(topic,row)





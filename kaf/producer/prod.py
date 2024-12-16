import csv
import json
from confluent_kafka import Producer

from database.mongo.repo import insert_data
from kaf.config_kafka import KAFKA_BROKER, STUDENTS_TOPIC, STUDENTS_COURSE_PERFORMANCE, STUDENTS_LIFESTYLE_TOPIC, \
    TEACHES_TOPIC, REVIEWS_TOPIC

producer = Producer({
    'bootstrap.servers': KAFKA_BROKER,
})


def send_to_kafka(topic, data):
    producer.produce(topic, value=json.dumps(data).encode('utf-8'))
    producer.flush()
    print(f"Sent message to Kafka: {data}")


def read_csv(topic,path):
    with open(path, 'r',encoding='utf-8') as f:
        data = csv.reader(f)
        for row in data:
            print(row)
            send_to_kafka(topic,row)

def chunk_data(data, chunk_size=1000):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def send_large_data_in_chunks(topic, data):
    for chunk in chunk_data(data):
        send_to_kafka(topic, chunk)




# read_csv(STUDENTS_TOPIC,'C:\\Users\\c0548\\PycharmProjects\\proj_data\\students-profiles.csv')
# read_csv(STUDENTS_COURSE_PERFORMANCE,'C:\\Users\\c0548\\PycharmProjects\\proj_data\\student_course_performance.csv')
# read_csv(STUDENTS_LIFESTYLE_TOPIC,'C:\\Users\\c0548\\PycharmProjects\\proj_data\\student_lifestyle.csv')
# insert_data('C:\\Users\\c0548\\PycharmProjects\\proj_data\\academic_network.json')
read_csv(REVIEWS_TOPIC,"C:\\Users\\c0548\\PycharmProjects\\proj_data\\reviews_with_students.csv")
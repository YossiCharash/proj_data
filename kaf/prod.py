import csv
import json
from confluent_kafka import Producer
from toolz import partition_all

from kaf.config_kafka import KAFKA_BROKER, STUDENTS_TOPIC, STUDENTS_COURSE_PERFORMANCE, STUDENTS_LIFESTYLE_TOPIC, \
    TEACHERS_TOPIC, REVIEWS_TOPIC, CLASSROOMS_TOPIC, RELATIONSHIPS_TOPIC

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
        next(data)
        for row in data:
            print(row)
            send_to_kafka(topic,row)

def read_json(path):
    with open(path, 'r',encoding='utf-8') as f:
        data = json.load(f)
        for row in data['teachers']:
            send_to_kafka(TEACHERS_TOPIC, row)
            print(row)

        for row in data['classes']:
            send_to_kafka(CLASSROOMS_TOPIC, row)
            print(row)

        for row in list(partition_all(10, data['relationships'])):
            send_to_kafka(RELATIONSHIPS_TOPIC, row)
            print(row)









# read_csv(STUDENTS_TOPIC,'../../data/students-profiles.csv')
# read_csv(STUDENTS_COURSE_PERFORMANCE,'../../data/student_course_performance.csv')
# read_csv(STUDENTS_LIFESTYLE_TOPIC,'../../data/student_lifestyle.csv')
read_json('../data/academic_network.json')
# read_csv(REVIEWS_TOPIC,"C:\\Users\\c0548\\PycharmProjects\\proj_data\\reviews_with_students.csv")
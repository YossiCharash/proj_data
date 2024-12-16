import json

from confluent_kafka import Consumer
from database.postgres.config_postgres import db_session
from database.postgres.models import Classrooms
from kaf.config_kafka import KAFKA_BROKER, CLASSROOMS_TOPIC

consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'school',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subscribe([CLASSROOMS_TOPIC])


def send_message():
    try:
        while True:
            message = consumer.poll(timeout=1.0)
            if message is None:
                continue

            if message.error():
                print(f"Error: {message.error()}")
                continue

            data = message.value().decode('utf-8')
            print("The data com and insert to database")
            insert_to_db(data)

    except KeyboardInterrupt:
        print("Process interrupted by user.")

    finally:
        consumer.close()
        print("Consumer closed.")


def insert_to_db(message):
    try:
        if message is not None:
            classrooms_data = json.loads(message)

            classrooms = Classrooms(
            id=classrooms_data['id'],
            course_name = classrooms_data['course_name'],
            section = classrooms_data['section'],
            department = classrooms_data['department'],
            semester = classrooms_data['semester'],
            room = classrooms_data['room'],
            schedule = classrooms_data['schedule'],
            teacher_id = classrooms_data['teacher_id'],
            )

            db_session.add(classrooms)
            db_session.commit()
            print(classrooms)
            print("the data inserted to database")

    except Exception as e:
        print(f"Error while inserting to DB: {e}")
        db_session.rollback()


if __name__ == '__main__':
    send_message()



import json

from confluent_kafka import Consumer
from database.postgres.config_postgres import db_session
from database.postgres.models import  StudentsLifestyle
from kaf.config_kafka import KAFKA_BROKER, STUDENTS_LIFESTYLE_TOPIC

consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'school',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subscribe([STUDENTS_LIFESTYLE_TOPIC])


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
            student_data = json.loads(message)

            course_performance = StudentsLifestyle(
                student_id=student_data[0],
                study_hours_per_day=student_data[1],
                extracurricular_hours_per_day=student_data[2],
                sleep_hours_per_day=student_data[3],
                social_hours_per_day=student_data[4],
                physical_activity_hours_per_day=student_data[5],
                gpa=student_data[6],
                stress_level=student_data[7]
            )

            db_session.add(course_performance)
            db_session.commit()
            print(course_performance)
            print("the data inserted to database")

    except Exception as e:
        print(f"Error while inserting to DB: {e}")
        db_session.rollback()


if __name__ == '__main__':
    send_message()



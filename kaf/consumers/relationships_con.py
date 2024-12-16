import json

from confluent_kafka import Consumer
from database.postgres.config_postgres import db_session
from database.postgres.models import Relationships
from kaf.config_kafka import KAFKA_BROKER, RELATIONSHIPS_TOPIC

consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'school',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subscribe([RELATIONSHIPS_TOPIC])


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
            relationships_data = json.loads(message)

            for row in relationships_data:

                relationships = Relationships(
                    student_id=row['student_id'],
                    class_id=row['class_id'],
                    teacher_id=row['teacher_id'],
                    enrollment_date=row['enrollment_date'],
                    relationship_type=row['relationship_type'],
                )

                db_session.add(relationships)
                db_session.commit()
                print(relationships)
                print("the data inserted to database")

    except Exception as e:
        print(f"Error while inserting to DB: {e}")
        db_session.rollback()


if __name__ == '__main__':
    send_message()



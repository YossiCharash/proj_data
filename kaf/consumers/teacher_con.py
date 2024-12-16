import json
from confluent_kafka import Consumer
from database.postgres.config_postgres import db_session
from database.postgres.models import  Teachers
from kaf.config_kafka import KAFKA_BROKER, TEACHERS_TOPIC

consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'school',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subscribe([TEACHERS_TOPIC])


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
            teachers_data = json.loads(message)
            teachers = Teachers(
            id=teachers_data['id'],
            name = teachers_data['name'],
            department = teachers_data['department'],
            title =teachers_data['title'],
            office = teachers_data['office'],
            email =teachers_data['email'],
            )

            db_session.add(teachers)
            db_session.commit()
            print(teachers)
            print("the data inserted to database")

    except Exception as e:
        print(f"Error while inserting to DB: {e}")
        db_session.rollback()


if __name__ == '__main__':
    send_message()



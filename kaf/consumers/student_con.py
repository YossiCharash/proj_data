import json

from confluent_kafka import Consumer
from database.postgres.config_postgres import db_session
from database.postgres.models import Students
from kaf.config_kafka import KAFKA_BROKER, STUDENTS_TOPIC

consumer_conf = {

    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'school',
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(consumer_conf)
consumer.subscribe([STUDENTS_TOPIC])

def send_message():
    try:
        while True:
            # Polling לקבלת הודעות מ-Kafka
            message = consumer.poll(timeout=1.0)  # פולינג עם זמן המתנה של שניה
            if message is None:
                continue  # אם אין הודעות, ממשיכים

            if message.error():
                print(f"Error: {message.error()}")
                continue  # אם יש שגיאה בהודעה, ממשיכים

            data = message.value().decode('utf-8')
            print("The data com and insert to database")
            # Insert הודעה למסד נתונים
            insert_to_db(data)

    except KeyboardInterrupt:
        print("Process interrupted by user.")

    finally:
        consumer.close()  # סגירת ה-consumer בסיום
        print("Consumer closed.")


def insert_to_db(message):
    try:
        if message is not None:  # לבדוק אם הודעה לא ריקה

            student_data = json.loads(message)
            if 'id' in student_data:
                del student_data['id']
            student = Students(
                id=student_data[0],
                first_name=student_data[1],
                last_name=student_data[2],
                age=student_data[3],
                address=student_data[4]
            )

            db_session.add(student)
            db_session.commit()
            print(student)
            print("the data inserted to database")

    except Exception as e:
        print(f"Error while inserting to DB: {e}")
        db_session.rollback()



if __name__ == '__main__':
    send_message()

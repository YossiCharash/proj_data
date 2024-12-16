import json

from confluent_kafka import Consumer
from database.postgres.config_postgres import db_session
from database.postgres.models import  StudentsCoursePerformance
from kaf.config_kafka import KAFKA_BROKER, STUDENTS_COURSE_PERFORMANCE

consumer_conf = {

    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'school',
    'auto.offset.reset': 'earliest'}


consumer = Consumer(consumer_conf)
consumer.subscribe([STUDENTS_COURSE_PERFORMANCE])



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


            lifestyle = StudentsCoursePerformance(
                student_id=student_data[0],
                course_name=student_data[1],
                current_grade=student_data[2],
                attendance_rate=student_data[3],
                assignments_completed=student_data[4],
                missed_deadlines=student_data[5],
                participation_score=student_data[6],
                midterm_grade=student_data[7],
                study_group_attendance=student_data[8],
                office_hours_visits=student_data[9],
                extra_credit_completed=student_data[10]
            )

            db_session.add(lifestyle)
            db_session.commit()
            print(lifestyle)
            print("the data inserted to database")

    except Exception as e:
        print(f"Error while inserting to DB: {e}")
        db_session.rollback()


if __name__ == '__main__':
    send_message()


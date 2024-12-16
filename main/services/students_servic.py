import pandas as pd
from database.postgres.config_postgres import db_session
from database.postgres.models import StudentsLifestyle, Students

def format_conversion(query):
    result = pd.DataFrame([item.__dict__ for item in query])
    return result


def remove_instance_state(data):
    return data.drop('_sa_instance_state', axis=1)


def find_by_gpa():

    lifestyle_df = format_conversion(db_session.query(StudentsLifestyle).all())
    student_df = format_conversion(db_session.query(Students).all())


    lifestyle_df = remove_instance_state(lifestyle_df)
    student_df = remove_instance_state(student_df)

    average_gpa = lifestyle_df['gpa'].mean()
    average_sleep = lifestyle_df['sleep_hours_per_day'].mean()
    merged_df = pd.merge(student_df, lifestyle_df)

    high_gpa_students = merged_df[
        (merged_df['gpa'] > average_gpa) &
        (merged_df['sleep_hours_per_day'] > average_sleep)
    ]

    print(high_gpa_students)

    return high_gpa_students



from flask import Blueprint, jsonify

from main.services.students_servic import find_by_gpa

Student = Blueprint('Student', __name__)

#Find students whose GPA is above average but sleep hours are below average
# - return full student’s profile, the GPA and the sleep hours.
@Student.route("/students_whose_GPA", methods=['GET'])
def get_students_by_gpa():
    try:
        high_gpa_students = find_by_gpa()
        result = high_gpa_students.to_dict(orient='records')
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return False,500

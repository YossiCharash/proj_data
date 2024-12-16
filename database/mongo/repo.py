import json

from database.mongo.config import db



def insert_data(path):
    with open(path, "r") as file:
        data = json.load(file)

    teachers = data.get("teachers", [])
    classes = data.get("classes", [])
    relationships = data.get("relationships", [])
    nested_data = []
    for teacher in teachers:
        teacher_id = teacher["id"]
        teacher_classes = [
            {
                **cls,
                "students": [
                    {
                        "student_id": rel["student_id"],
                        "enrollment_date": rel["enrollment_date"],
                        "relationship_type": rel["relationship_type"]
                    }
                    for rel in relationships if rel["class_id"] == cls["id"]
                ]
            }
            for cls in classes if cls["teacher_id"] == teacher_id
        ]
        nested_teacher = {
            **teacher,
            "classes": teacher_classes
        }
        nested_data.append(nested_teacher)
    db.teachers.insert_many(nested_data)

    print("Nested data inserted successfully!")

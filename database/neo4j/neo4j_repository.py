



class PhoneTrackerRepository:
    def __init__(self,driver):
        self.driver = driver


    def insert_review(self,data):
        with self.driver.session() as session:
            for teacher in data['teachers']:
                session.run("""
                    CREATE (t:Teacher {
                        id: $id, 
                        name: $name,
                        department: $department,
                        title: $title,
                        office: $office,
                        email: $email
                    })
                """,id=teacher['id'], name=teacher['name'],
                    department=teacher['department'],title=teacher['title'],
                            office=teacher['office'], email=teacher['email'])

            for classroom in data['classes']:
                session.run("""
                    CREATE (c:Classroom {
                    id: $id, 
                    course_name: $course_name,
                    section: $section,
                   department: $department,
                   semester: $semester,
                   room: $room,
                   schedule: $schedule,
                   teacher_id: $teacher_id,
                     })
                """, id=classroom['id'], course_name=classroom['course_name'],
                            section=classroom['section'], department=classroom['department'],
                            semester=classroom['semester'], room=classroom['room'],
                            schedule=classroom['schedule'], teacher_id=classroom['teacher_id'])


            for connection in data['relationships']:
                session.run("""
                            MERGE (student:Student {id: $student_id})
                            MERGE (class:Class {id: $class_id})
                            MERGE (teacher:Teacher {id: $teacher_id})

                            CREATE (student)-[r:$relationship_type {
                                enrollment_date: $enrollment_date
                            }]->(class)

                            CREATE (teacher)-[:TEACHES]->(class)
                        """, {
                    'student_id': connection['student_id'],
                    'class_id': connection['class_id'],
                    'teacher_id': connection['teacher_id'],
                    'enrollment_date': connection['enrollment_date'],
                    'relationship_type': connection['relationship_type']
                })




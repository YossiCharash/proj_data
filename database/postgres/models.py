from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, TIMESTAMP
from sqlalchemy.orm import relationship
from database.postgres.config_postgres import engine

Base = declarative_base()



class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    address = Column(String(200), nullable=False)

    lifestyle = relationship('StudentsLifestyle', back_populates='student')
    course_performance = relationship('StudentsCoursePerformance', back_populates='student')
    relationships = relationship('Relationships', back_populates='student')




class StudentsLifestyle(Base):
    __tablename__ = 'students_lifestyle'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)  # תיקון ל-ForeignKey
    study_hours_per_day = Column(Float, nullable=False)
    extracurricular_hours_per_day = Column(Float, nullable=False)
    sleep_hours_per_day = Column(Float, nullable=False)
    social_hours_per_day = Column(Float, nullable=False)
    physical_activity_hours_per_day = Column(Float, nullable=False)
    gpa = Column(Float, nullable=False)
    stress_level = Column(String(10), nullable=False)

    student = relationship('Students', back_populates='lifestyle')




class StudentsCoursePerformance(Base):
    __tablename__ = 'students_course_performance'  # שינוי שם למחלקה בשיטת PEP8
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)  # תיקון ל-ForeignKey
    course_name = Column(String(20), nullable=False)
    current_grade = Column(Float, nullable=False)
    attendance_rate = Column(Float, nullable=False)
    assignments_completed = Column(Integer, nullable=False)
    missed_deadlines = Column(Integer, nullable=False)
    participation_score = Column(Float, nullable=False)
    midterm_grade = Column(Float, nullable=False)
    study_group_attendance = Column(Integer, nullable=False)
    office_hours_visits = Column(Integer, nullable=False)
    extra_credit_completed = Column(Integer, nullable=False)

    student = relationship("Students", back_populates="course_performance")


class Teachers(Base):
    __tablename__ = 'teachers'
    id = Column(String(10), primary_key=True)
    name = Column(String(20), nullable=False)
    department = Column(String(20), nullable=False)
    title = Column(String(20), nullable=False)
    office = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)

    classroom = relationship('Classrooms', back_populates='teacher')
    relationships = relationship('Relationships', back_populates='teacher')



class Classrooms(Base):
    __tablename__ = 'classrooms'
    id = Column(String(10), primary_key=True)
    course_name = Column(String(20), nullable=False)
    section = Column(Integer, nullable=False)
    department = Column(String(20), nullable=False)
    semester = Column(String(20), nullable=False)
    room = Column(String(20), nullable=False)
    schedule = Column(String(20), nullable=False)
    teacher_id = Column(String(10), ForeignKey('teachers.id'), nullable=False)

    teacher = relationship("Teachers", back_populates="classroom")
    relationships = relationship('Relationships', back_populates='classroom')

class Relationships(Base):
    __tablename__ = 'relationships'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    class_id = Column(String(10), ForeignKey('classrooms.id'), nullable=False)
    teacher_id = Column(String(10), ForeignKey('teachers.id'), nullable=False)
    enrollment_date = Column(TIMESTAMP, nullable=False)
    relationship_type = Column(String(12),nullable=False)

    teacher = relationship("Teachers", back_populates="relationships")
    student = relationship("Students", back_populates="relationships")
    classroom = relationship("Classrooms", back_populates="relationships")




def init_db():
    Base.metadata.create_all(engine)

init_db()

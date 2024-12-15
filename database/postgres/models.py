from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, BigInteger, Text, Float
from sqlalchemy.orm import relationship
from enum import Enum



Base = declarative_base()

class StatusStressLevel(Enum):
    Moderate = 'Moderate'
    Low = 'Low'
    High = 'High'



class Students(Base):
    __tablename__ = 'students'
    id = Column(BigInteger, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    address = Column(String(200), nullable=False)


class StudentsLifestyle(Base):
    __tablename__ = 'students_lifestyle'
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    study_hours_per_day = Column(Float, nullable=False)
    extracurricular_hours_per_day = Column(Float, nullable=False)
    sleep_hours_per_day = Column(Float, nullable=False)
    social_hours_per_day = Column(Float, nullable=False)
    physical_activity_hours_per_day = Column(Float, nullable=False)
    gpa = Column(Float, nullable=False)
    stress_level = Column(Enum(StatusStressLevel), nullable=False)

    student = relationship('Student', backref='students_lifestyle')



class studentCoursePerformance(Base):
     __tablename__ = 'students_course_performance'
     student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
     course_name = Column(String(20), nullable=False)
     current_grade = Column(Float, nullable=False)
     attendance_rate = Column(Float, nullable=False)
     assignments_completed = Column(Integer, nullable=False)
     missed_deadlines = Column(Integer, nullable=False)
     participation_score = Column(Float, nullable=False)
     midterm_grade = Column(Float, nullable=False)
     study_group_attendance =Column(Integer, nullable=False)
     office_hours_visits = Column(Integer, nullable=False)
     extra_credit_completed =Column(Integer, nullable=False)

     student = relationship("Students", back_populates="students_course_performance")


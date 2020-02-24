from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, UnicodeText, ForeignKey, Float, desc, func
from cs_student import db

class Student(db.Model):
    __tablename__ = 'student'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, ForeignKey('course.id'))
    phone = db.Column(db.String)
    email = db.Column(db.Text)
    # logs = db.relationship('Logs', backref="student", lazy=True)

    def total_point(self):
        return db.session.query(func.sum(Logs.point)).filter_by(student_id=self.id).first()[0]
    
class Course(db.Model):
    __tablename__ = 'course'
    
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String, nullable=False)
    cohort = db.Column(db.String, nullable=False)

class Logs(db.Model):
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, ForeignKey('student.id'))
    activities = db.Column(db.String, nullable=False)
    point = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

class Attendance(db.Model):
    __tablename__= 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, ForeignKey('student.id'))
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)


db.create_all()
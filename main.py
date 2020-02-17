from flask import Flask, render_template, redirect, url_for, request,jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Text, UnicodeText, ForeignKey, Float, desc, func
import requests
import json
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'somekey'
db = SQLAlchemy(app)

# Other static variable: 
ATTENDANCE_POINT = 10
LATE_POINT = -10

class Student(db.Model):
    __tablename__ = 'student'
    
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText, nullable=False)
    course_id = db.Column(db.UnicodeText, ForeignKey('course.course_id'))
    last_login = db.Column(db.Date, nullable=False, default=datetime.utcnow)


class Course(db.Model):
    __tablename__ = 'course'
    
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.UnicodeText, nullable=False)

class Logs(db.Model):
    __tablename__ = 'logs'
    
    log_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, ForeignKey('student.student_id'))
    activities = db.Column(db.UnicodeText, nullable=False)
    point_gain = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    total_point = db.Column(db.Integer, nullable=False)

class Point(db.Model):
    __tablename__= 'point'

    student_id = db.Column(db.Integer, ForeignKey('logs.student_id'), primary_key=True)
    log_id = db.Column(db.Integer, ForeignKey('logs.log_id'), primary_key=True)
    total_point = db.Column(db.Integer, nullable=False)

# class PointForm(FlaskForm):
#     point = IntegerField('Add/Remove Point')
#     activities = StringField('Activities')
#     checkin = BooleanField('Check-in')
#     submit = SubmitField('Submit')




@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    all_students = []
    all_students = db.session.query(Logs.student_id, Student.name, func.max(Logs.total_point), Logs.date).join(Student).group_by(Logs.student_id).order_by(desc(Logs.total_point)).all()
    if request.method == 'GET':
        return render_template('home.html', all_students=all_students)
    elif request.method == 'POST':
        student_data = request.get_json()
        for data in student_data:
            # print(data['id'], type(data['checkin']))
            if data['checkin']:
                # print('chekin success')
                latest_point = Logs.query.with_entities(Logs.total_point).filter_by(student_id=data['id']).order_by(desc(Logs.log_id)).first()[0]
                attendance = Logs(student_id=data['id'], activities='Attendance', point_gain=ATTENDANCE_POINT, total_point=latest_point + int(ATTENDANCE_POINT) )
                db.session.add(attendance)
                db.session.commit()
                # print('end of getting attendance')
            if data['activity']!='' or data['point'] != '': 
                # print('other activities success')
                latest_point = Logs.query.with_entities(Logs.total_point).filter_by(student_id=data['id']).order_by(desc(Logs.log_id)).first()[0]
                new_log = Logs(student_id=data['id'], activities=data['activity'], point_gain=int(data['point']), total_point=latest_point + int(data['point']) )
                db.session.add(new_log)
                db.session.commit()
        resp = jsonify(success=True)
        return resp
    
@app.route('/log')
def log():
    log_data = db.session.query(Logs, Student.name).join(Student).order_by(desc(Logs.log_id)).limit(50).all()
    return render_template('log.html', log_data=log_data)

@app.route('/student')
def func_name():
    student_data = db.session.query(Student, Course.course_name).join(Course).all()
    print(student_data)
    return render_template('student.html', students=student_data)
if __name__ == '__main__':
    app.run(debug=True)

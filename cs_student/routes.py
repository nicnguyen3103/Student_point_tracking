from datetime import datetime
from flask import render_template, redirect, url_for, request,jsonify
from cs_student import app, db
from cs_student.forms import AddStudent
from cs_student.models import Student, Course, Logs, Attendance
from sqlalchemy import func,desc
import requests
import json
import os 
import gspread 
from oauth2client.service_account import ServiceAccountCredentials


# Other static variable: 
ATTENDANCE_POINT = 10
LATE_POINT = -10
SPREADSHEET_KEY = '17N5hWt0Eup-tG5HmjKzd7blk_wquVVwHZau7Q_zhGp4'

credential = os.environ.get("GOOGLE_API_CREDENTIALS")


def get_credentials():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] #Spectify the API that you want to have access to
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential, scope) #give the credentials form the json file you just download 
    return credentials

gc = gspread.authorize(get_credentials())
sheet = gc.open_by_key(SPREADSHEET_KEY)
wks_log = sheet.worksheet("Log")

def get_credentials():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] #Spectify the API that you want to have access to
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential, scope) #give the credentials form the json file you just download 
    return credentials

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    all_students = []
    last_log = db.session.query(Attendance.student_id, func.max(Attendance.date).label("date")).group_by(Attendance.student_id).subquery()
    all_students = db.session.query(Student, func.sum(Logs.point).label("total_point"), Logs.date).join(Logs).join(last_log).group_by(Student.id).order_by(desc('total_point'), desc(Logs.id)).all()
    if request.method == 'GET':Logs.date
        return render_template('home.html', all_students=all_students)
    elif request.method == 'POST':
        student_data = request.get_json()
        print(student_data)
        for data in student_data:
            if data['checkin']:
                attendance = Logs(student_id=data['id'], activities='Attendance', point=ATTENDANCE_POINT)
                checkin = Attendance(student_id=data['id'])
                db.session.add(checkin)
                db.session.add(attendance)
                db.session.commit()

                student_name = Student.query.get_or_404(data['id'])
                print(student_name.name)

                wks_log.append_row([datetime.utcnow().strftime('%d-%m-%Y'), student_name.name, 10, "Attendance"], value_input_option='RAW')

            if data['activity']!='' or data['point'] != '': 
                new_log = Logs(student_id=data['id'], activities=data['activity'], point=int(data['point']))
                db.session.add(new_log)
                db.session.commit()

                student_name = Student.query.get_or_404(data['id'])
                wks_log.append_row([datetime.utcnow().strftime('%d-%m-%Y'), student_name.name, int(data['point']), data['activity'], data['note']], value_input_option='RAW')

        resp = jsonify(success=True)
        return resp
    
@app.route('/log')
def log():
    log_data = db.session.query(Logs, Student.name).join(Student).order_by(desc(Logs.id)).limit(50).all()
    return render_template('log.html', log_data=log_data)

@app.route('/student')
def student():
    student_data = db.session.query(Student, Course.cohort).join(Course).all()
    return render_template('student.html', students=student_data)

@app.route('/delete/<int:student_id>',methods=['POST'])
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    log = Logs.query.get_or_404(student_id)
    attendance = Attendance.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.delete(log)
    db.session.delete(attendance)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddStudent()
    if form.validate_on_submit():
        course_id = db.session.query(Course).filter(Course.cohort.like('%Tonga')).first()

        new_student = Student(name=form.name.data, phone=form.phone.data, 
        email=form.email.data, course_id=course_id.id)

        db.session.add(new_student)
        db.session.commit()
        # init_student
        student = db.session.query(Student).order_by(desc(Student.id)).first()
        new_log = Logs(student_id=student.id, activities='init_student', point=100)
        db.session.add(new_log)
        db.session.commit()
        # add attendance 
        checkin = Attendance(student_id=student.id)
        db.session.add(checkin)
        db.session.commit()
        return redirect('/student')
    return render_template('add.html', form=form)
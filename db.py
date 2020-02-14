from main import db
from main import Student, Course, Logs
db.create_all()

student_1 = Student(name='Nguyet Do', course_id=1)
student_2 = Student(name='An Dang', course_id=1)
student_3 = Student(name='Kieu Tuan Anh', course_id=1)
student_4 = Student(name='Tobias Becher', course_id=1)

log_1 = Logs(student_id= 1, activities='init_student', point_gain=100, total_point=100)
log_2 = Logs(student_id= 2, activities='init_student', point_gain=100, total_point=100)
log_3 = Logs(student_id= 3, activities='init_student', point_gain=100, total_point=100)
log_4 = Logs(student_id= 4, activities='init_student', point_gain=100, total_point=100)
log_5 = Logs(student_id=1, activities='kaggle', point_gain=10, total_point=110)
# point_1 = Point(student_id=1, log_id=1, total_point=100)
# point_2 = Point(student_id=2, log_id=2, total_point=100)
# point_3 = Point(student_id=3, log_id=3, total_point=100)
# point_4 = Point(student_id=4, log_id=4, total_point=100)

course_1 = Course(course_name='Tonga')
db.session.add(student_1)
db.session.add(student_2)
db.session.add(student_3)
db.session.add(student_4)

db.session.add(log_1)
db.session.add(log_2)
db.session.add(log_3)
db.session.add(log_4)
db.session.add(log_5)

db.session.add(course_1)
# db.session.add(point_1)
# db.session.add(point_2)
# db.session.add(point_3)
# db.session.add(point_4)

db.session.commit()
# Accesible through Postman 

import sqlite3
import random
from datetime import datetime
from flask import Flask, request, jsonify, Blueprint, session
from flask_cors import CORS

students_api = Blueprint('students_api', __name__)
CORS(students_api, resources={r"/*": {"origins": "*"}})

    
def connect_to_db():
    conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db')
    return conn

def insert_student(student):
    inserted_student = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''INSERT INTO Students (Student_id, Student_name, Other_details, Username, Password, Studentnumber) 
                       VALUES (?, ?, ?, ?, ?, ?)''', 
                    (student['Student_id'], student['Student_name'], student['Other_details'], 
                     student['Username'], student['Password'], student['Studentnumber']))
        conn.commit()
        inserted_student = get_student_by_id(cur.lastrowid)
    except:
        conn.rollback()
    finally:
        conn.close()

    return inserted_student

def get_students():
    students = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Students")
        rows = cur.fetchall()

        for i in rows:
            student = {}
            student["Student_id"] = i["Student_id"]
            student["Student_name"] = i["Student_name"]
            student["Other_details"] = i["Other_details"]
            student["Class_id"] = i["Class_id"]
            student["Username"] = i["Username"]
            student["Password"] = i["Password"]
            student["Studentnumber"] = i["Studentnumber"]
            students.append(student)
    except:
        students = []

    return students

def get_student_by_id(student_id):
    student = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Students WHERE Student_id = ?", 
                    (student_id,))
        row = cur.fetchone()

        student["Student_id"] = row["Student_id"]
        student["Student_name"] = row["Student_name"]
        student["Other_details"] = row["Other_details"]
        student["Class_id"] = i["Class_id"]
        student["Username"] = row["Username"]
        student["Password"] = row["Password"]
        student["Studentnumber"] = row["Studentnumber"]
    except:
        student = {}

    return student

def update_student(student):
    updated_student = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''UPDATE Students SET Student_name = ?, Other_details = ?, Class_id = ?,Username = ?, Password = ?, Studentnumber = ?
                       WHERE Student_id = ?''',
                    (student["Student_name"], student["Other_details"], student["Class_id"], student["Username"], 
                     student["Password"], student["Studentnumber"], student["Student_id"],))
        conn.commit()
        updated_student = get_student_by_id(student["Student_id"])
    except:
        conn.rollback()
        updated_student = {}
    finally:
        conn.close()

    return updated_student

def delete_student(student_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Students WHERE Student_id = ?",     
                      (student_id,))
        conn.commit()
        message["status"] = "Student deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete Student"
    finally:
        conn.close()

    return message

def insert_faculty(faculty):
    inserted_faculty = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''INSERT INTO Faculty (Faculty_id, Faculty_name, Faculty_email, Other_details, Username, Password) 
                       VALUES (?, ?, ?, ?, ?, ?)''', 
                    (faculty['Faculty_id'], faculty['Faculty_name'], faculty['Faculty_email'], 
                     faculty['Other_details'], faculty['Username'], faculty['Password']))
        conn.commit()
        inserted_faculty = get_faculty_by_id(cur.lastrowid)
    except:
        conn.rollback()
    finally:
        conn.close()

    return inserted_faculty

def get_faculties():
    faculties = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Faculty")
        rows = cur.fetchall()

        for i in rows:
            faculty = {}
            faculty["Faculty_id"] = i["Faculty_id"]
            faculty["Faculty_name"] = i["Faculty_name"]
            faculty["Faculty_email"] = i["Faculty_email"]
            faculty["Other_details"] = i["Other_details"]
            faculty["Username"] = i["Username"]
            faculty["Password"] = i["Password"]
            faculties.append(faculty)
    except:
        faculties = []

    return faculties

def get_faculty_by_id(faculty_id):
    faculty = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Faculty WHERE Faculty_id = ?", 
                    (faculty_id,))
        row = cur.fetchone()

        faculty["Faculty_id"] = row["Faculty_id"]
        faculty["Faculty_name"] = row["Faculty_name"]
        faculty["Faculty_email"] = row["Faculty_email"]
        faculty["Other_details"] = row["Other_details"]
        faculty["Username"] = row["Username"]
        faculty["Password"] = row["Password"]
    except:
        faculty = {}

    return faculty

def update_faculty(faculty):
    updated_faculty = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''UPDATE Faculty SET Faculty_name = ?, Faculty_email = ?, Other_details = ?, Username = ?, Password = ?
                       WHERE Faculty_id = ?''',
                    (faculty["Faculty_name"], faculty["Faculty_email"], faculty["Other_details"], 
                     faculty["Username"], faculty["Password"], faculty["Faculty_id"],))
        conn.commit()
        updated_faculty = get_faculty_by_id(faculty["Faculty_id"])
    except:
        conn.rollback()
        updated_faculty = {}
    finally:
        conn.close()

    return updated_faculty

def delete_faculty(faculty_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Faculty WHERE Faculty_id = ?",     
                      (faculty_id,))
        conn.commit()
        message["status"] = "Faculty deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete Faculty"
    finally:
        conn.close()

    return message

def insert_schedule(schedule):
    inserted_schedule = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''INSERT INTO schedule (schedule_id, course_id, faculty_id, room_id, start_time, end_time, days) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                    (schedule['schedule_id'], schedule['course_id'], schedule['faculty_id'], 
                     schedule['room_id'], schedule['start_time'], schedule['end_time'], schedule['days']))
        conn.commit()
        inserted_schedule = get_schedule_by_id(cur.lastrowid)
    except:
        conn.rollback()
    finally:
        conn.close()

    return inserted_schedule

def get_schedule():
    schedules = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Schedule")
        rows = cur.fetchall()

        
        for i in rows:
            schedule = {}
            schedule["schedule_id"] = i["schedule_id"]
            schedule["course_id"] = i["course_id"]
            schedule["faculty_id"] = i["faculty_id"]
            schedule["room_id"] = i["room_id"]
            schedule["start_time"] = i["start_time"]
            schedule["end_time"] = i["end_time"]
            schedule["days"] = i["days"]
            schedules.append(schedule)
    except:
        schedules = []

    return schedules

def get_schedule_by_id(schedule_id):
    schedule = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Schedule WHERE Schedule_id = ?", 
                    (schedule_id,))
        row = cur.fetchone()

        
        schedule["schedule_id"] = row["schedule_id"]
        schedule["course_id"] = row["course_id"]
        schedule["faculty_id"] = row["faculty_id"]
        schedule["room_id"] = row["room_id"]
        schedule["start_time"] = row["start_time"]
        schedule["end_time"] = row["end_time"]
        schedule["days"] = row["days"]
    except:
        schedule = {}

    return schedule

def update_schedule(schedule):
    updated_schedule = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''UPDATE Schedule SET course_id = ?, faculty_id = ?, room_id = ?, start_time = ?, end_time = ?, days = ?
                       WHERE Schedule_id = ?''',
                    (schedule["Course_id"], schedule["Faculty_id"], schedule["Room_id"], 
                     schedule["Start_time"], schedule["End_time"], schedule["Schedule_id"], schedule["Days"]))
        conn.commit()

        updated_schedule = get_schedule_by_id(schedule["Schedule_id"])
    except:
        conn.rollback()
        updated_schedule = {}
    finally:
        conn.close()

    return updated_schedule

def update_schedule_by_id(schedule_id, schedule):
    updated_schedule = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''UPDATE schedule SET course_id = ?, faculty_id = ?, room_id = ?, start_time = ?, end_time = ?, days = ?
                       WHERE Schedule_id = ?''',
                    (schedule["course_id"], schedule["faculty_id"], schedule["room_id"], 
                     schedule["start_time"], schedule["end_time"], schedule["days"], schedule_id))
        conn.commit()
        updated_schedule = get_schedule_by_id(schedule_id)
    except:
        conn.rollback()
        updated_schedule = {}
    finally:
        conn.close()

    return updated_schedule

def delete_schedule(schedule_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Schedule WHERE Schedule_id = ?",     
                      (schedule_id,))
        conn.commit()
        message["status"] = "Schedule deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete Schedule"
    finally:
        conn.close()

    return message



@students_api.route('/api/students', methods=['GET'])
def api_get_students():
    return jsonify(get_students())

@students_api.route('/api/students/<student_id>', methods=['GET'])
def api_get_student(student_id):
    return jsonify(get_student_by_id(student_id))

@students_api.route('/api/students/add', methods=['POST'])
def api_add_student():
    student = request.get_json()
    return jsonify(insert_student(student))

@students_api.route('/api/students/update', methods=['PUT'])
def api_update_student():
    student = request.get_json()
    return jsonify(update_student(student))

@students_api.route('/api/students/delete/<student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    return jsonify(delete_student(student_id))

@students_api.route('/api/faculties', methods=['GET'])
def api_get_faculties():
    return jsonify(get_faculties())

@students_api.route('/api/faculties/<faculty_id>', methods=['GET'])
def api_get_faculty(faculty_id):
    return jsonify(get_faculty_by_id(faculty_id))

@students_api.route('/api/faculties/add', methods=['POST'])
def api_add_faculty():
    faculty = request.get_json()
    return jsonify(insert_faculty(faculty))

@students_api.route('/api/faculties/update', methods=['PUT'])
def api_update_faculty():
    faculty = request.get_json()
    return jsonify(update_faculty(faculty))

@students_api.route('/api/faculties/delete/<faculty_id>', methods=['DELETE'])
def api_delete_faculty(faculty_id):
    return jsonify(delete_faculty(faculty_id))

@students_api.route('/api/schedule', methods=['GET'])
def api_get_schedule():
    return jsonify(get_schedule())

@students_api.route('/api/schedule/<schedule_id>', methods=['GET'])
def api_get_schedule_by_id(schedule_id):
    return jsonify(get_schedule_by_id(schedule_id))

@students_api.route('/api/schedule/add', methods=['POST'])
def api_add_schedule():
    schedule = request.get_json()
    return jsonify(insert_schedule(schedule))

@students_api.route('/api/schedule/update', methods=['PUT'])
def api_update_schedule():
    schedule = request.get_json()
    return jsonify(update_schedule(schedule))

@students_api.route('/api/schedule/update/<schedule_id>', methods=['PUT'])
def api_update_by_id_schedule(schedule_id):
    schedule = request.get_json()
    return jsonify(update_schedule_by_id(schedule_id, schedule))

@students_api.route('/api/schedule/delete/<schedule_id>', methods=['DELETE'])
def api_delete_schedule(schedule_id):
    return jsonify(delete_schedule(schedule_id))

@students_api.route('/api/checkin/<int:student>', methods=['POST'])
def api_checkin(student):
    data = request.json
    attendance_date = datetime.now().strftime('%Y-%m-%d')
    attendance_time = datetime.now().strftime('%H:%M:%S')
    status = data.get('status')
    question = data.get('question')
    answer = data.get('answer')
    reason = data.get('reason')

    
    conn = connect_to_db()
    cursor = conn.cursor()
    student_query = cursor.execute('SELECT * FROM Students WHERE Studentnumber = ?', (student,))
    student_data = student_query.fetchone()
    if not student_data:
        return jsonify({'error': f'Student {student} not found'}), 404

    
    cursor.execute('INSERT INTO Attendance (Student_id, Studentnumber, Attendance_date, Attendance_time, Status, Question, Answer, Reason) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (student_data[0], student_data[5], attendance_date, attendance_time, status, question, answer, reason))
    conn.commit()
    conn.close()

    return jsonify({'message': f'Student {student} checked in successfully'}), 200

@students_api.route('/api/questions/random', methods=['GET'])
def get_random_question():
    questions = ['Wat is de hoofdstad van Frankrijk?', 'Hoe heet Adriaan zijn compagnon?"', 'Wat is de hoogste berg ter wereld?', 'Wat is de hoofstad van Nederland?']
    question = random.choice(questions)
    return jsonify({'question': question})


@students_api.route('/api/attendance', methods=['GET'])
def get_attendance():
    conn = connect_to_db()
    cursor = conn.cursor()

    # Retrieve attendance records from the database
    cursor.execute('SELECT Students.student_name, Students.studentnumber, Attendance.Attendance_date, Attendance.Attendance_time, Attendance.Status, Students.Class_id FROM Students INNER JOIN Attendance ON Students.Student_id=Attendance.Student_id')
    rows = cursor.fetchall()

    # Convert the records into a list of dictionaries
    attendance = []
    for row in rows:
        attendance.append({
            'student_name': row[0],
            'studentnumber': row[1],
            'date': row[2],
            'time': row[3],
            'status': row[4],
            'class_id': row[5]
        })
    conn.close()
    
    return jsonify({'attendance': attendance})

from flask import Flask, request, jsonify, Blueprint, session, redirect, render_template, url_for, flash
from flask_cors import CORS
import datetime
import sqlite3
import socket

admin = Blueprint('admin', __name__)

conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db', check_same_thread=False)
c = conn.cursor()


# Route to display all students in a HTML table
@admin.route('/admin/students', methods=['GET'])
def admin_students():
    c.execute("SELECT * FROM Students")
    students = c.fetchall()
    return render_template('admin/admin_students.html', students=students)


@admin.route('/admin/students/add', methods=['GET'])
def add_student_form():
    return render_template('admin/admin_add_students.html')

# Route to add a new student
@admin.route('/admin/students/add', methods=['POST'])
def add_student():
    student_name = request.form['student_name']
    other_details = request.form['other_details']
    username = request.form['username']
    password = request.form['password']
    student_number = request.form['student_number']
    class_id = request.form['class_id']

    c.execute("INSERT INTO students (student_name, other_details, username, password, studentnumber, class_id) VALUES (?, ?, ?, ?, ?, ?)",
              (student_name, other_details, username, password, student_number, class_id))
    conn.commit()

    return admin_students()

# Route to update an existing student
@admin.route('/admin/students/update', methods=['POST'])
def update_student():
    student_id = request.form['student_id']
    student_name = request.form['student_name']
    other_details = request.form['other_details']
    username = request.form['username']
    password = request.form['password']
    student_number = request.form['student_number']
    class_id = request.form['class_id']

    c.execute("UPDATE students SET student_name = ?, other_details = ?, username = ?, password = ?, student_number = ?, class_id = ? WHERE student_id = ?",
              (student_name, other_details, username, password, student_number, class_id, student_id))
    conn.commit()

    return admin_students()

@admin.route('/admin/students/update/<int:student_id>', methods=['GET', 'POST'])
def update_student_per_id(student_id=None):
    if request.method == 'POST':
        student_name = request.form['student_name']
        other_details = request.form['other_details']
        username = request.form['username']
        password = request.form['password']
        student_number = request.form['student_number']
        class_id = request.form['class_id']

        c.execute("UPDATE students SET student_name = ?, other_details = ?, username = ?, password = ?, studentnumber = ?, class_id = ? WHERE student_id = ?",
                  (student_name, other_details, username, password, student_number, class_id, student_id))
        conn.commit()

        return admin_students()
    else:
        c.execute("SELECT * FROM Students WHERE student_id = ?", (student_id,))
        student = c.fetchone()
        return render_template('admin/admin_update_students.html', student=student)

# Route to delete a student
@admin.route('/admin/students/delete', methods=['POST'])
def delete_student():
    student_id = request.form['student_id']

    c.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()

    return admin_students()

# Route to display all faculties in an HTML table
@admin.route('/admin/faculties', methods=['GET'])
def admin_faculties():
    c.execute("SELECT * FROM Faculty")
    faculties = c.fetchall()
    return render_template('admin/admin_faculties.html', faculties=faculties)

@admin.route('/admin/faculties/add', methods=['GET'])
def add_faculty_form():
    return render_template('admin_add_faculties.html')

# Route to add a new faculty
@admin.route('/admin/faculties/add', methods=['POST'])
def add_faculty():
    faculty_name = request.form['faculty_name']
    faculty_email = request.form['faculty_email']
    other_details = request.form['other_details']
    username = request.form['username']
    password = request.form['password']

    c.execute("INSERT INTO faculty (faculty_name, faculty_email, other_details, username, password) VALUES (?, ?, ?, ?, ?)",
              (faculty_name, faculty_email, other_details, username, password))
    conn.commit()

    return admin_faculties()

# Route to update an existing faculty
@admin.route('/admin/faculties/update', methods=['POST'])
def update_faculty():
    faculty_id = request.form['faculty_id']
    faculty_name = request.form['faculty_name']
    faculty_email = request.form['faculty_email']
    other_details = request.form['other_details']
    username = request.form['username']
    password = request.form['password']

    c.execute("UPDATE faculty SET faculty_name = ?, faculty_email = ?, other_details = ?, username = ?, password = ? WHERE faculty_id = ?",
              (faculty_name, faculty_email, other_details, username, password, faculty_id))
    conn.commit()

    return admin_faculties()

@admin.route('/admin/faculties/update/<int:faculty_id>', methods=['GET', 'POST'])
def update_faculty_per_id(faculty_id=None):
    if request.method == 'POST':
        faculty_name = request.form['faculty_name']
        faculty_email = request.form['faculty_email']
        other_details = request.form['other_details']
        username = request.form['username']
        password = request.form['password']

        c.execute("UPDATE faculty SET faculty_name = ?, faculty_email = ?, other_details = ?, username = ?, password = ? WHERE faculty_id = ?",
                  (faculty_name, faculty_email, other_details, username, password, faculty_id))
        conn.commit()

        return admin_faculties()
    else:
        c.execute("SELECT * FROM Faculty WHERE faculty_id = ?", (faculty_id,))
        faculty = c.fetchone()
        return render_template('admin/admin_update_faculties.html', faculty=faculty)

# Route to delete a faculty
@admin.route('/admin/faculties/delete', methods=['POST'])
def delete_faculty():
    faculty_id = request.form['faculty_id']

    c.execute("DELETE FROM faculty WHERE faculty_id = ?", (faculty_id,))
    conn.commit()

    return admin_faculties()

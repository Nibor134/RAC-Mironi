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
    return render_template('admin_students.html', students=students)


@admin.route('/admin/students/add', methods=['GET'])
def add_student_form():
    return render_template('admin_add_students.html')

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
        return render_template('admin_update_students.html', student=student)

# Route to delete a student
@admin.route('/admin/students/delete', methods=['POST'])
def delete_student():
    student_id = request.form['student_id']

    c.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()

    return admin_students()
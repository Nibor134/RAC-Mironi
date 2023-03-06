
from flask import Flask, request, jsonify, Blueprint, session, redirect, render_template, url_for, flash
from flask_cors import CORS
import datetime
import sqlite3
import socket

teacher = Blueprint('teacher', __name__)

@teacher.route('/create_class', methods=['GET', 'POST'])
def create_class():
    if 'teacher_logged_in' in session:
        if request.method == 'POST':
            # Get form data
            class_name = request.form['class_name']
            date = request.form['date']
            time = request.form['time']
            location = request.form['location']
            
            # Insert class details into the database
            conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db')
            c = conn.cursor()
            c.execute('INSERT INTO clas (class_name, date, time, location) VALUES (?, ?, ?, ?)', (class_name, date, time, location))
            conn.commit()
            conn.close()
            
            return redirect(url_for('teacher_dashboard'))
            
        return render_template('create_class.html')
    else:
        flash('Log alstublieft eerst in', 'danger')
        return redirect(url_for('login'))

@teacher.route('/view_classes')
def view_classes():
    if 'teacher_logged_in' in session:
        conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Schedule')
        classes = c.fetchall()
        conn.close()
        return render_template('view_classes2.html', classes=classes)
    else:
        flash('Log alstublieft eerst in', 'danger')
        return redirect(url_for('login'))

@teacher.route('/aanwezigheid', methods=['GET', 'POST'])
def attendance():
    if 'teacher_logged_in' in session:
        print(session)
        return render_template('aanwezigheid.html')
    else:
        flash('Log alstublieft eerst in', 'danger')
        return redirect(url_for('login'))

@teacher.route('/meetings/<int:meeting_id>')
def meeting(meeting_id):
    hostname = socket.gethostname()

    ip_address = socket.gethostbyname(hostname)
    ip_str = str(ip_address)
    

    # Connect to the database
    conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db')
    c = conn.cursor()

    # Retrieve the meeting with the requested ID from the database
    c.execute('SELECT * FROM Meeting WHERE Meeting_id = ?', (meeting_id,))
    meeting = c.fetchone()

    # Close the database connection
    conn.close()

    # Render the meeting template with the meeting data
    return render_template('meetings.html', meeting=meeting, ip_str=ip_str, meeting_id=meeting_id )


@teacher.route('/create_meeting')
def make_meeting():
    
    return render_template('create_meeting.html')

@teacher.route('/teacher/upcoming_meetings')
def t_upcoming_meetings():
    return render_template('teacher_upcoming_meetings.html')

@teacher.route('/teacher/all_meetings')
def t_all_meetings():
    return render_template('teacher_all_meetings.html')
from flask import Flask, render_template, request, session, redirect, url_for,flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-secret-key'


conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db', check_same_thread=False)
c = conn.cursor()


@app.route('/')
def index():
    return render_template('login.html')

# Student dashboard
@app.route('/student_dashboard')
def student_dashboard():
    if 'student_logged_in' in session:
        student_id = session.get('user_id')
        return render_template('dashboard.html',)
    else:
        flash('Invalid login credentials.', 'danger')
        return redirect(url_for('login'))

@app.route('/teacher_dashboard')
def teacher_dashboard():
    teacher_id = session.get('user_id')
    if 'teacher_logged_in' in session:
        return render_template('teacher_dashboard.html',)
    else:
        flash('Invalid login credentials.', 'danger')
        return redirect(url_for('login'))

def get_student_by_studentnumber(studentnumber):
    conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Studentnumber, Password FROM Students WHERE Studentnumber = ?", (studentnumber,))
    student = cursor.fetchone()
    conn.close()
    if student:
        return {'studentnumber': student[0], 'password': student[1]}
    else:
        return None

def get_teacher_by_email(email):
    conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db')
    c = conn.cursor()
    c.execute('SELECT faculty_email, Password FROM faculty WHERE faculty_email = ?', (email,))
    teacher = c.fetchone()
    conn.close()
    if teacher:
        return {'email': teacher[0], 'password': teacher[1]}
    else:
        return None

def get_admin_by_username(username):
    conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db')
    c = conn.cursor()
    c.execute('SELECT * FROM admins WHERE username = ?', (username,))
    admin = c.fetchone()
    conn.close()
    if admin:
        return {'username': admin[0], 'password': admin[1]}
    else:
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        if role == 'student':
            # Validate student login
            student = get_student_by_studentnumber(username)
            if student and student['password'] == password:
                session.clear()
                session['student_logged_in'] = True
                session['username'] = student['studentnumber']
                flash('You were successfully logged in!', 'success')
                return redirect(url_for('student_dashboard'))
            else:
                flash('Invalid login credentials.', 'danger')
                return redirect(url_for('login'))

        elif role == 'teacher':
            # Validate teacher login
            teacher = get_teacher_by_email(username)
            if teacher and teacher['password'] == password:
                session.clear()
                session['teacher_logged_in'] = True
                session['username'] = teacher['email']
                flash('You were successfully logged in!', 'success')
                return redirect(url_for('teacher_dashboard'))
            else:
                flash('Invalid login credentials.', 'danger')
                return redirect(url_for('login'))

        elif role == 'admin':
            # Validate admin login
            admin = get_admin_by_username(username)
            if admin and admin['password'] == password:
                session.clear()
                session['admin_logged_in'] = True
                session['username'] = admin['username']
                flash('You were successfully logged in!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid login credentials.', 'danger')
                return redirect(url_for('login'))
    
    return render_template('login_test.html')

@app.route('/dashboard')
def dashboard():
    if 'student_logged_in' in session:
        return render_template('student_dashboard.html')
    elif 'teacher_logged_in' in session:
        return render_template('teacher_dashboard.html')
    elif 'admin_logged_in' in session:
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/teacher')
def teacher():
    if 'teacher_logged_in' in session:
        return render_template('teacher_dashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if 'admin_logged_in' in session:
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

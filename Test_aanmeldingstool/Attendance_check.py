import datetime
import os.path
import sqlite3
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from lib.tablemodel import DatabaseModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HogeschoolRotterdam'
socketio = SocketIO(app)

attendance = {}
start_time = datetime.time(9, 0)  # 9:00 AM
end_time = datetime.time(17, 0)  # 5:00 PM

DATABASE = os.path.join(app.root_path, 'databases', 'test_database.db')
dbm = DatabaseModel(DATABASE)

conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database.db') 
c = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main.html')

@socketio.on('checkin')
def on_checkin(data):
    student_name = data['student_name']
    attendance[student_name] = True
    socketio.emit('attendance', list(attendance.keys()), broadcast=True)

@app.route('/attendance', methods=['GET', 'POST'])
def attendance_list():
    return render_template('attendance.html', attendance=attendance)

@app.route('/export', methods=['GET', 'POST'])
def export_attendance():
    if request.method == 'POST':
        class_name = request.form.get('class_name')
        now = datetime.datetime.now()
        date_string = now.strftime('%Y%m%d')
        time_string = now.strftime('%H:%M:%S')
        filename = 'Test_aanmeldingstool/databases/test_database.db'
        table_name = class_name + '_' + date_string 

        conn = sqlite3.connect(filename)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS {} (student_name text)".format(table_name))
        for student_name in attendance:
            c.execute("INSERT INTO {} (student_name) VALUES (?)".format(table_name), (student_name,))
        conn.commit()
        conn.close()

        return 'Attendance data exported to {}'.format(filename)
    else:
        return render_template('export.html')

# Route for All Tables
@app.route("/tables")
def all():
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE
    )

# The table route displays the content of a table
@app.route("/table_details/<table_name>")
def table_content(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "table_details.html", rows=rows, columns=column_names, table_name=table_name
        )

if __name__ == '__main__':
    socketio.run(app, debug=True)
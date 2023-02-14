import sqlite3
from flask import Flask, request, jsonify #added to top of file
from flask_cors import CORS #added to top of file

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def connect_to_db():
    conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database.db')
    return conn

def insert_student(student):
    inserted_student = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''INSERT INTO Studenten (Student_id, Voornaam, Achternaam, Studentnummer)
        VALUES (?, ?, ?, ?, ?)", 
        (Student['Student_id'], Student['Voornaam'], Student['Achternaam'], Student['Studentnummer']) ''')
        conn.commit()
        inserted_student = get_student_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_student


def get_studenten():
    Studenten = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Studenten")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            student = {}
            student["Student_id"] = i["Student_id"]
            student["Voornaam"] = i["Voornaam"]
            student["Achternaam"] = i["Achternaam"]
            student["Studentnummer"] = i["Studentnummer"]
            student.append(student)

    except:
        Studenten = []

    return Studenten

def get_student_by_id(student_id):
    student = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Studenten WHERE Student_id = ?", 
                       (student_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        student["Student_id"] = row["Student_id"]
        student["Voornaam"] = row["Voornaam"]
        student["Achternaam"] = row["Achternaam"]
        student["Studentnummer"] = row["Studentnummer"]
    except:
        student = {}

    return student

def update_student(student):
    updated_student = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''UPDATE Studenten SET voornaam = ?, Achternaam = ?, Studentnummer = 
                     ? WHERE student_id = ?",  
                     (student["Voornaam"], student["Achternaam"], student["Studentnummer"],
                     student["Student_id"],)''')
        conn.commit()
        #return the student
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
        conn.execute("DELETE from Studenten WHERE Student_id = ?",     
                      (student_id,))
        conn.commit()
        message["status"] = "Student deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete Student"
    finally:
        conn.close()

    return message



@app.route('/api/studenten', methods=['GET'])
def api_get_studenten():
    return jsonify(get_studenten())

@app.route('/api/studenten/<student_id>', methods=['GET'])
def api_get_student(student_id):
    return jsonify(get_student_by_id(student_id))

@app.route('/api/studenten/add',  methods = ['POST'])
def api_add_student():
    student = request.get_json()
    return jsonify(insert_student(student))

@app.route('/api/studenten/update',  methods = ['PUT'])
def api_update_student():
    student = request.get_json()
    return jsonify(update_student(student))

@app.route('/api/studenten/delete/<student_id>',  methods = ['DELETE'])
def api_delete_student(student_id):
    return jsonify(delete_student(student_id))

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
    app.run() #run app

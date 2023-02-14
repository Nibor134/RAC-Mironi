import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def connect_to_db():
    conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database.db')
    return conn

def insert_docent(docent):
    inserted_docent = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''INSERT INTO Docenten (Docent_id, Voornaam, Achternaam, Email, Telefoonnummer) 
                       VALUES (?, ?, ?, ?, ?)''', 
                    (docent['Docent_id'], docent['Voornaam'], docent['Achternaam'], 
                     docent['Email'], docent['Telefoonnummer']))
        conn.commit()
        inserted_docent = get_docent_by_id(cur.lastrowid)
    except:
        conn.rollback()
    finally:
        conn.close()

    return inserted_docent

def get_docenten():
    docenten = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Docenten")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            docent = {}
            docent["Docent_id"] = i["Docent_id"]
            #docent["Voornaam"] = i["Voornaam"]
            #docent["Achternaam"] = i["Achternaam"]
            #docent["Email"] = i["Email"]
            #docent["Telefoonnummer"] = i["Telefoonnummer"]
            docenten.append(docent)
    except:
        docenten = []

    return docenten

def get_docent_by_id(docent_id):
    docent = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Docenten WHERE Docent_id = ?", 
                    (docent_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        docent["Docent_id"] = row["Docent_id"]
        #docent["Voornaam"] = row["Voornaam"]
        #docent["Achternaam"] = row["Achternaam"]
        #docent["Email"] = row["Email"]
        #docent["Telefoonnummer"] = row["Telefoonnummer"]
    except:
        docent = {}

    return docent

def update_docent(docent):
    updated_docent = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''UPDATE Docenten SET Voornaam = ?, Achternaam = ?, Email = ?, Telefoonnummer = ?
                       WHERE Docent_id = ?''',
                    (docent["Voornaam"], docent["Achternaam"], docent["Email"], 
                     docent["Telefoonnummer"], docent["Docent_id"],))
        conn.commit()
        #return the docent
        updated_docent = get_docent_by_id(docent["Docent_id"])
    except:
        conn.rollback()
        updated_docent = {}
    finally:
        conn.close()

    return updated_docent

def delete_docent(docent_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from Docenten WHERE Docent_id = ?",     
                      (docent_id,))
        conn.commit()
        message["status"] = "Docent deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete Docent"
    finally:
        conn.close()

    return message

@app.route('/api/docenten', methods=['GET'])
def api_get_docenten():
    return jsonify(get_docenten())

@app.route('/api/docenten/<docent_id>', methods=['GET'])
def api_get_docent(docent_id):
    return jsonify(get_docent_by_id(docent_id))

@app.route('/api/docenten/add', methods=['POST'])
def api_add_docent():
    docent = request.get_json()
    return jsonify(insert_docent(docent))

@app.route('/api/docenten/update', methods=['PUT'])
def api_update_docent():
    docent = request.get_json()
    return jsonify(update_docent(docent))

@app.route('/api/docenten/delete/<docent_id>', methods=['DELETE'])
def api_delete_docent(docent_id):
    return jsonify(delete_docent(docent_id))

if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
    app.run()

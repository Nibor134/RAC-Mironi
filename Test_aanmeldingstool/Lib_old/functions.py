def get_db_connection():
    import sqlite3
    
    try:
        connection = sqlite3.connect('Test_aanmeldingstool/databases/test_database.db')
        print("Working")
    except sqlite3.OperationalError as e:
        print(f"Error opening database file {'Test_aanmeldingstool/databases/test_database.db'}")
        raise e

    return connection

def login_check():
    from flask import request

    username = request.form.get('Username')
    password = request.form.get('Password')

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('''
                   SELECT Studenten.Voornaam || ' ' || Studenten.Achternaam AS student_naam,
                   Docenten.docent_voornaam || ' ' || Docenten.docent_achternaam AS docent_naam, 
                   Beheerder.beheerder_voornaam || ' ' || Beheerder.beheerder_achternaam AS beheerder_naam 
                   FROM Studenten, Docenten, Beheerder 
                   WHERE student_naam='%s' AND Studentnummer='%s' OR docent_naam ='%s' AND Docenten.docent_wachtwoord ='%s' OR beheerder_naam ='%s' AND Beheerder.beheerder_wachtwoord ='%s' 
                   ''' % (username, password, username, password, username, password))
    data = cursor.fetchall()
    connection.close()

    if len(data)==0:
        print("Login Failed")
        granted = False
    else:
        print("Login Successful")
        granted = True

    return granted
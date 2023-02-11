import sqlite3
import os.path

conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database') 
c = conn.cursor()
                   
          
c.execute('''
          INSERT INTO Studenten (Student_id, Voornaam, Achternaam, Studentnummer)

                VALUES
                (1,'Jan', 'Pieters', '1234567'),
                (2,'Kees', 'Konings', '3231525'),
                (3,'Dominique', 'Jansen' ,'5325234')
          ''')
conn.commit()
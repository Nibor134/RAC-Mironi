import sqlite3
import os.path

conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database.db') 
c = conn.cursor()
                   
          
c.execute('''
          CREATE TABLE IF NOT EXISTS Docenten
          ([docent_id] INTEGER PRIMARY KEY, [docent_voornaam] TEXT, [docent_achternaam] TEXT, [docent_wachtwoord] TEXT)
          ''')
conn.commit()
import sqlite3
import os.path

conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database.db') 
c = conn.cursor()

c.execute('''
          INSERT INTO Docenten (docent_id, docent_voornaam, docent_achternaam, docent_wachtwoord)

          VALUES
          (1, 'Jan', 'Korter', 'test1')
          ''')
conn.commit()
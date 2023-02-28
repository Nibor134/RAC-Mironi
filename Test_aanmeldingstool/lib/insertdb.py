import sqlite3
import os.path

conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db') 
c = conn.cursor()

c.execute('''CREATE TABLE Meeting
                    (Meeting_id INTEGER PRIMARY KEY,
                    Meeting_title TEXT,
                    Meeting_date DATE,
                    Meeting_time TIME,
                    Meeting_duration INTEGER,
                    Meeting_location TEXT,
                    Meeting_description TEXT,
                    Created_by TEXT,
                    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    Updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

conn.commit()
conn.close()
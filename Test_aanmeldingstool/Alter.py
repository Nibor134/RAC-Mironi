import sqlite3

# Connect to the database
conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db')
cursor = conn.cursor()

# Add columns to the attendance table
cursor.execute('ALTER TABLE Attendance ADD COLUMN Studentnumber TEXT')
cursor.execute('ALTER TABLE Attendance ADD COLUMN Question TEXT')
cursor.execute('ALTER TABLE Attendance ADD COLUMN Answer TEXT')
cursor.execute('ALTER TABLE Attendance ADD COLUMN Reason TEXT')

# Commit the changes and close the connection
conn.commit()
conn.close()

import sqlite3

# Connect to the database
conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db')
cursor = conn.cursor()

# Add columns to the attendance table
cursor.execute('ALTER TABLE Attendance ADD COLUMN Class_id INTEGER')


# Commit the changes and close the connection
conn.commit()
conn.close()

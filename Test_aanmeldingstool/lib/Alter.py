import sqlite3

# Connect to the database
conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db')
c = conn.cursor()

# Add the Meeting_id column to the Attendance table
c.execute('ALTER TABLE Attendance ADD COLUMN class_id INTEGER REFERENCES Students(class_id)')

# Commit the changes and close the database connection
conn.commit()
conn.close()
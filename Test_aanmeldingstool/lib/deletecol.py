import sqlite3

# Connect to the database
conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db')
c = conn.cursor()

# Delete the class_id column from the Meeting table
c.execute('ALTER TABLE Meeting DROP COLUMN class_id')

# Commit the changes and close the database connection
conn.commit()
conn.close()

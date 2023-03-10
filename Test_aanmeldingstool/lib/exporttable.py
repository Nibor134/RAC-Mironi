import sqlite3
import csv
import os

# Connect to the database
conn = sqlite3.connect('Test_aanmeldingstool/databases/attendence.db')
cursor = conn.cursor()

# Define a list of table names to export
table_names = ['Students', 'Faculty', 'Attendance' , 'Meeting', 'Class', 'Courses', 'Schedule']

# Create a subdirectory for the exports
export_dir = 'exports'
if not os.path.exists(export_dir):
    os.makedirs(export_dir)

# Export data from each table to CSV file
for table_name in table_names:
    cursor.execute(f'SELECT * FROM {table_name}')
    col_names = [cn[0] for cn in cursor.description]
    rows = cursor.fetchall()

    # Export data to CSV file
    with open(f'{table_name}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(col_names)
        writer.writerows(rows)

# Close the database connection
conn.close()

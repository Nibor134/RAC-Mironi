
import sqlite3
  

conn = sqlite3.connect('Test_aanmeldingstool/databases/test_database.db') 
c = conn.cursor()
  
# create table named address of customers with
# 4 columns id,name age and address
# drop table
conn.execute("DROP TABLE docenten")
  
# close the connection
conn.close()
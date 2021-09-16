import pyodbc

conn = pyodbc.connect(
    r'data/database/data')
cursor = conn.cursor()
cursor.execute('select * from products')

for row in cursor.fetchall():
    print(row)
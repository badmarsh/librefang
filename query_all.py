import sqlite3

conn = sqlite3.connect('/home/ubuntu/.librefang/data/librefang.db')
cursor = conn.cursor()

cursor.execute("SELECT id, workflow_name, state, error FROM workflow_runs;")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()

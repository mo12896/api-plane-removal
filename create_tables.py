import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS pointclouds (id INTEGER PRIMARY KEY, filename TEXT, file BLOB)"
cursor.execute(create_table)

connection.commit()

connection.close()
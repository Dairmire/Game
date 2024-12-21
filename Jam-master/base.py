import sqlite3

db = sqlite3.connect('tab.db')

c = db.cursor()

c.execute('''CREATE TABLE users (
    name text,
    password text
)''')

c.execute("INSERT INTO users VALUES ('admin', 'ad12')")

db.commit()

db.close()
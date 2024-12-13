import sqlite3

connection = sqlite3.connect('leader_board.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
guessed_cards INTEGER,
time INTEGER
)
''')

#cursor.execute("DELETE FROM Users")
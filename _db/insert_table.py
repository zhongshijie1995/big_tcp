import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.executescript(open('create.sql', 'r', encoding='utf-8').read())

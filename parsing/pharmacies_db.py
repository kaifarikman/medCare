import sqlite3


def get_connection():
    conn = sqlite3.connect('pharmacies.db')
    return conn


def start_session():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS pharmacies(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                cords TEXT
            );'''
        )


def all_pharmacies():
    with get_connection() as conn:
        cur = conn.cursor()
        full = cur.execute('''SELECT name, cords FROM pharmacies''').fetchall()
        conn.commit()
        return full


def add_pharmacy(pharmacy, cord):
    with get_connection() as conn:
        flag = False
        for i in all_pharmacies():
            if i == (pharmacy, cord):
                flag = False
        if not flag:
            cur = conn.cursor()
            cur.execute('''INSERT INTO pharmacies (name, cords) VALUES(?, ?)''', (pharmacy, cord))


def unique_db():
    with get_connection() as conn:
        cur = conn.cursor()
        values = list(set(all_pharmacies()))
        values.sort()
        cur.execute('''DELETE FROM pharmacies''')
        for i in values:
            cur.execute('''INSERT INTO pharmacies (name, cords) VALUES(?, ?)''', i)
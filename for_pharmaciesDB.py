import sqlite3


def get_connection():
    conn = sqlite3.connect('parsing/pharmacies.db')
    return conn


def all_pharmacies():
    with get_connection() as conn:
        cur = conn.cursor()
        full = cur.execute('''SELECT name, cords FROM pharmacies''').fetchall()
        conn.commit()
        return full


import sqlite3


def get_connection():
    conn = sqlite3.connect('db.db')
    return conn


def start_session():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                login TEXT,
                password TEXT
            )'''
        )


def all_db():
    with get_connection() as conn:
        cur = conn.cursor()
        full = cur.execute('''SELECT id, name, surname, login, password FROM users''').fetchall()
        return full


def add_user(data):
    with get_connection() as conn:
        cur = conn.cursor()
        logins = [i[0] for i in cur.execute('''SELECT login FROM users''').fetchall()]
        if data[2] in logins:
            return False
        cur.execute('''INSERT INTO users (name, surname, login, password) VALUES(?, ?, ?, ?)''', data)
        return True


def get_user(login, password):
    with get_connection() as conn:
        cur = conn.cursor()
        data = cur.execute(
            '''SELECT name, surname, login, password FROM users WHERE login=? AND password=?''',
            (login, password)
        ).fetchall()
        if not data:
            return False
        return data


def change_user(data, new_data):
    '''Для смены имени и фамилии пользователя(settings.ui)'''
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(f'UPDATE users SET name=?, surname=? WHERE login={data[0][2]} AND password={data[0][3]}',
                    new_data[0][:2])
        '''Передается имя, фамилия, почта, пароль и новое имя, новая фамилия'''

        '''Поменять старое имя и фамилию на новые'''
        return new_data


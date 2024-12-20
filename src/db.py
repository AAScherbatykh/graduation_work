import sqlite3


def create_database():
    """ Функция создания базы данных."""

    connection = sqlite3.connect('task_manager.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT NOT NULL,
    deadline DATETIME NOT NULL,
    status TEXT NOT NULL,
    created_at DATETIME NOT NULL
    )''')

    connection.commit()
    cursor.close()
    connection.close()

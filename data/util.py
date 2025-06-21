import sqlite3


def get_connection():
    conn = None
    try:
        conn = sqlite3.connect("dados.db")
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
    except sqlite3.Error as e:
        print(e)
    return conn
    
import sqlite3
from datetime import datetime, timedelta

today = datetime.now().date()

try:
    conn = sqlite3.connect('data/database.db')
    cursor = conn.cursor()
    print("База данных успешно подключена к SQLite")
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)

def join(chat_id, username, firstname, date):
    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?", [chat_id]
    )
    data = cursor.fetchone()

    if data is None:
        cursor.execute(
            "INSERT INTO users (user_id, username, firstname, date) VALUES (?,?,?,?)", (chat_id, username, firstname, date)
        )
        conn.commit()
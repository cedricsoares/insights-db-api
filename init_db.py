import os
import sqlite3


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
API_FOLDER_PATH = os.path.join(ROOT_PATH, "api")
DB_FILE_PATH = os.path.join(API_FOLDER_PATH, "database.db")
SQL_FOLDER_PATH = os.path.join(API_FOLDER_PATH, "sql")
SCHEMA_FILE_PATH = os.path.join(SQL_FOLDER_PATH, "schema.sql")


def init_db():
    conn = sqlite3.connect(DB_FILE_PATH)
    cur = conn.cursor()
    with open(SCHEMA_FILE_PATH) as f:
        cur.executescript(f.read())
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()

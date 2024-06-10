import sqlite3
from api.constants import DB_PATH, DB_SCHEMA_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    with open(DB_SCHEMA_PATH) as f:
        cur.executescript(f.read())
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()

import pytest
import sqlite3

from api.app import app as flask_app
from tests.constants import DB_SCHEMA_PATH


@pytest.fixture
def client():
    client = flask_app.test_client()

    yield client


@pytest.fixture
def db_connection():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    with open(DB_SCHEMA_PATH) as f:
        cur.executescript(f.read())
        cur.execute("INSERT INTO pages (id, name) VALUES (?, ?)", (11, "fake_name"))
        conn.commit()
        cur.execute(
            "INSERT INTO videos (id, page_id, title) VALUES (?, ?, ?)",
            (11, 11, "fake_title"),
        )
        conn.commit()
        cur.execute(
            "INSERT INTO video_insights (id, video_id, likes, views) VALUES (?, ?, ?, ?)",
            (11, 11, 11, 11),
        )
        conn.commit()

    yield conn
    conn.close()

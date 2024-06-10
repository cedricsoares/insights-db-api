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
        cur.execute("INSERT INTO pages (id, name) VALUES (?, ?)", (1, "fake_name"))
        conn.commit()

    yield conn
    conn.close()

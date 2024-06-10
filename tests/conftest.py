import pytest
import sqlite3
from api.app import app as flask_app
from tests.constants import DB_SCHEMA_PATH


@pytest.fixture()
def app():
    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def session():
    conn = sqlite3.connect(":memory:")
    db_session = conn.cursor()
    yield db_session
    conn.close()


@pytest.fixture()
def setup_db(session):
    with open(DB_SCHEMA_PATH) as f:
        session.executesscripts(f.read)
        session.connection.commit()

import os
import tempfile

import pytest
from app import create_app
from app.database import db

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_path,
        }
    )

    with app.app_context():
        db.create_all()
        sql = ""
        for line in _data_sql:
            if not line.startswith("--") and line.strip("\n"):
                sql += line.strip("\n")
                if sql.endswith(";"):
                    try:
                        db.session.execute(sql)
                        db.session.commit()
                    except:
                        print("NG")
                    finally:
                        sql = ""

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

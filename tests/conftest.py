import os
import pytest
from api import create_app
from api.database import db_drop_and_create_all


@pytest.fixture
def app():
    database_filename = "poetry-db.db"
    database_path = "sqlite:///{}".format(
        os.path.join("./", database_filename)
    )
    flask_app = create_app(database_path=database_path)
    db_drop_and_create_all()
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()

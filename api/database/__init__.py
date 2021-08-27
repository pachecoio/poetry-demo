import json
import os

from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship

database_name = os.environ.get("DB") or "poetry-demo"
user = os.environ.get("USER") or "postgres"
password = os.environ.get("PASSWORD") or "root"
host = "db"
port = "5432"
DATABASE_PATH = os.environ.get("DATABASE_PATH") or "postgresql://{}:{}@{}:{}/{}".format(
    user, password, host, port, database_name
)


db = SQLAlchemy()
# import models to initialize them
import api.models


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

def setup_db(app, database_path=DATABASE_PATH):
    """
    setup_db(app)
    binds a flask application and a SQLAlchemy service
    """
    print("connect to db {}".format(database_path))
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()

    return db

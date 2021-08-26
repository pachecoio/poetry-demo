from sqlalchemy import Column, Integer, String

from api.database import db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

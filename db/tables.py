from sqlalchemy import Column, Integer, String

from .base import Database


class User(Database.BASE):
    __tablename__ = 'USERS'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    ref = Column(String)


class Remind(Database.BASE):
    __tablename__ = 'REMINDERS'

    id = Column(Integer, primary_key=True)
    user = Column(Integer)
    timedate = Column(String)
    text = Column(String)


def register_models():
    Database.BASE.metadata.create_all(Database().engine)

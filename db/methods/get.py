from sqlalchemy import exc

from ..base import Database
from ..tables import User, Remind


def get_user_by_id(_id: int) -> User:
    try:
        return Database().session.query(User).filter(User.id == _id).one()
    except exc.NoResultFound:
        return None


def get_user_by_telegram_id(telegram_id: int) -> User:
    try:
        return Database().session.query(User).filter(User.id == telegram_id).one()
    except exc.NoResultFound:
        return None


def get_all_users() -> list[User]:
    try:
        return Database().session.query(User).all()
    except exc.NoResultFound:
        return None


def get_users_with_admin() -> list[User]:
    try:
        return Database().session.query(User).filter(User.isAdmin == 1).all()
    except exc.NoResultFound:
        return None


def get_remind(timedate: str) -> list[Remind]:
    try:
        return Database().session.query(Remind).filter(Remind.timedate == timedate).all()
    except exc.NoResultFound:
        return None


def get_remind_id(pos_id: int) -> list[Remind]:
    try:
        return Database().session.query(Remind).filter(Remind.id == pos_id).one()
    except exc.NoResultFound:
        return None


def get_count() -> int:
    return Database().session.query(User).count()

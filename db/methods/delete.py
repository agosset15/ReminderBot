from ..base import Database
from ..tables import Remind
from .get import get_user_by_telegram_id, get_remind_id


def delete_user(telegram_id: int):
    session = Database().session
    user = get_user_by_telegram_id(telegram_id)

    if user:
        session.delete(user)
        session.commit()


def clear_remind():
    session = Database().session
    session.query(Remind).delete()


def delete_remind(id: int):
    session = Database().session
    schedule = get_remind_id(id)


    if schedule:
        session.delete(schedule)
        session.commit()

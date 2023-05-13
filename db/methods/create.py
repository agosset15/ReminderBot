import sqlalchemy.exc

from ..base import Database
from ..tables import User, Remind


def create_user(telegram_id: int, name: str, uname: str, ref: str) -> None:
    session = Database().session
    try:
        session.query(User.id).filter(User.id == telegram_id).one()
    except sqlalchemy.exc.NoResultFound:
        session.add(User(id=telegram_id, name=name, username=uname, ref=ref))
        session.commit()


def create_remind(user_id: int, timedate: str, text: str) -> None:
    session = Database().session
    try:
        session.query(Remind).filter(Remind.user == user_id, Remind.timedate == timedate,
                                     Remind.text == text).one()
    except sqlalchemy.exc.NoResultFound:
        session.add(Remind(user=user_id, timedate=timedate, text=text))
        session.commit()

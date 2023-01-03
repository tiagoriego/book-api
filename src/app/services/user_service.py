from config.db import Session
from schemas.user import User

session = Session()


def get_all_user() -> User:
    users = session.query(User).all()
    return users


def get_user_by_username(username: str) -> User:
    user = session.query(User).filter_by(username=username, disabled=False).first()
    return user

def get_user_by_id(id: str) -> User:
    user = session.query(User).filter_by(id=id, disabled=False).first()
    return user

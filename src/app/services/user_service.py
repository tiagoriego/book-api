from config.db import Session
from schemas.user import User

session = Session()


def get_all_user() -> User:
    users = session.query(User).all()
    return users


def get_user_by_username(username: str) -> User:
    user = session.query(User).filter_by(
        username=username, disabled=False).first()
    return user


def get_user_by_id(id: str) -> User:
    user = session.query(User).filter_by(id=id, disabled=False).first()
    return user


def get_user_by_email(email: str) -> User:
    user = session.query(User).filter_by(email=email).first()
    return user


def update_partial_user(id: str, full_name: str, email: str) -> bool:
    old_user = get_user_by_id(id)
    if old_user:
        old_user.full_name = full_name
        old_user.email = email
        try:
            session.add(old_user)
            session.flush()
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception("Failed update_partial_user", e)
        return True
    else:
        return False


def update_user_password(id: str, hashed_password: str):
    old_user = get_user_by_id(id)
    if old_user:
        old_user.hashed_password = hashed_password
        try:
            session.add(old_user)
            session.flush()
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception("Failed update_user_password", e)
        return True
    else:
        return False


def add_user(user: User):
    try:
        session.add(user)
        session.flush()
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception("Failed add_user", e)
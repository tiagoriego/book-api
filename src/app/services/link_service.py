from config.db import Session
from schemas.link import Link

session = Session()


def get_all_link(book_id: str) -> list[Link]:
    links = session.query(Link).filter_by(book_id=book_id).order_by(Link.created_at.desc()).all()
    return links


def get_link_by_id(link_id: str) -> Link:
    link = session.query(Link).filter_by(id=link_id).first()
    return link


def create_link(link: Link) -> Link:
    try:
        session.add(link)
        session.flush()
        link_id = str(link.id)
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception("Failed create_link", e)
    new_link = session.query(Link).filter_by(id=link_id).first()
    return new_link


def delete_link(link_id: str):
    try:
        session.query(Link).filter_by(id=link_id).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception("Failed delete_link", e)

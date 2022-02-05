from SessionManager import Session
from data.models.user import User
from data.models.cat import Cat


def raise_error(error, session=None):
    if session:
        session.close()
    return {"message": error}, 1


def db_is_null():
    session = Session()
    a, b = session.query(Cat).all(), session.query(User).all()
    f = a and b and len(a) > 0 and len(b) > 0
    session.close()
    return not f
from flask_restful import abort


def raise_error(error, session=None):
    if session:
        session.close()
    abort(400, message=error)

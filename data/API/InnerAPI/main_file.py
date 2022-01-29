def raise_error(error, session=None):
    if session:
        session.close()
    return {"message": error}, 1

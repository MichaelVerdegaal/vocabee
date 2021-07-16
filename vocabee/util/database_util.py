def init_db(db):
    """
    Create tables that don't exist
    :param db: database object
    """
    db.create_all()
    db.session.commit()

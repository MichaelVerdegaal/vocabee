from flask_security import hash_password

from vocabee import db, user_datastore


def create_user():
    if not user_datastore.find_user(email="test@me.com"):
        user_datastore.create_user(email="test@me.com", password=hash_password("password"))
    db.session.commit()

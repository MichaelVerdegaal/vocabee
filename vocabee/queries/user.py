from flask_security import hash_password

from vocabee import db, user_datastore


def setup_test_users():
    """
    Placeholder function to create some tests accounts
    """
    admin_user = user_datastore.find_user(email="admin@me.com")
    if not admin_user:
        user_datastore.create_user(email="admin@me.com", password=hash_password("password"), roles=['admin'])
    editor_user = user_datastore.find_user(email="editor@me.com")
    if not editor_user:
        user_datastore.create_user(email="editor@me.com", password=hash_password("password"), roles=['editor'])
    normal_user = user_datastore.find_user(email="user@me.com")
    if not normal_user:
        user_datastore.create_user(email="user@me.com", password=hash_password("password"), roles=['user'])
    db.session.commit()


def setup_roles():
    """
    Sets up the user roles, if they haven't been created already.
    """
    user_datastore.find_or_create_role(
        name="admin",
        permissions=["admin-read", "admin-write", "editor-read", "editor-write", "user-read", "user-write"],
    )
    user_datastore.find_or_create_role(
        name="editor", permissions=["editor-read", "editor-write", "user-read", "user-write"]
    )
    user_datastore.find_or_create_role(
        name="user", permissions=["user-read", "user-write"]
    )
    db.session.commit()

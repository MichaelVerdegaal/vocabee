import base64

from email_validator import validate_email, EmailNotValidError
from flask_security import hash_password

from vocabee import db, user_datastore
from vocabee.util.view_util import create_status


# TODO: remove this when account functionality is finished
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
    user_datastore.find_or_create_role(name="admin",
                                       permissions=["admin-read", "admin-write", "editor-read", "editor-write",
                                                    "user-read", "user-write"])
    user_datastore.find_or_create_role(name="editor",
                                       permissions=["editor-read", "editor-write", "user-read", "user-write"])
    user_datastore.find_or_create_role(name="user", permissions=["user-read", "user-write"])
    db.session.commit()


def register_user(email, username, password, roles=None):
    """
    Registers a user if it complies with all the checks
    :param email: email address
    :param username: username to display
    :param password: password
    :param roles: user roles
    :return: status message. This one also specifies what action to take for the front-end, and also a user-readable
    error-message if applicable
    """
    if roles is None:
        roles = ['user']

    # Check for existing accounts
    if user_datastore.find_user(email=email) or user_datastore.find_user(username=username):
        return create_status(400, description="An account with this email already exists", continue_register='false')

    # Validate email and normalize
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e:
        return create_status(400, description=f"{str(e)}", continue_register='false')

    # Check for empty fields, these shouldn't be possible if the front-end validated correctly, but can't hurt to check
    if not username:
        return create_status(400, description="Username can't be empty", continue_register='false')
    if not password:
        return create_status(400, description="Password can't be empty", continue_register='false')

    # Decode and hash password
    unobfuscated_password = base64.b64decode(password)
    hashed_password = hash_password(unobfuscated_password)

    # Register the user to the database
    user_datastore.create_user(email=email, username=username, password=hashed_password, roles=roles)
    db.session.commit()
    return create_status(200, continue_register='true')

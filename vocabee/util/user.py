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


def validate_register_fields(email, username, password, password_repeat):
    """
    Validates all the fields in the register field
    :param email: email address
    :param username: username to display
    :param password: password
    :param password_repeat: password repeated
    :return: continue_register boolean, field check report , email (normalized if applicable)
    """
    def set_field_invalid(field, error):
        """Quick helper function for the fields to lessen the amount of code"""
        fields[field]['valid'] = 'false'
        fields[field]['error'].append(error)

    continue_register = True
    fields = {field: {'valid': 'true', 'error': []} for field in ['email', 'username', 'password', 'password_repeat']}

    # Check for existing accounts
    if user_datastore.find_user(email=email) or user_datastore.find_user(username=username):
        set_field_invalid('email', "An account with this email already exists")

    # Validate email and normalize
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e:
        set_field_invalid('email', f"{str(e)}")

    # Check for empty fields, these shouldn't be possible if the front-end validated correctly, but can't hurt to check
    if not username:
        set_field_invalid('username', "Username field can't be empty")
    if not password:
        set_field_invalid('password', "Password field can't be empty")
    if not password_repeat:
        set_field_invalid('password_repeat', "Password repeat field can't be empty")

    if password != password_repeat:
        set_field_invalid('password', "The passwords don't match")
        set_field_invalid('password_repeat', "The passwords don't match")

    return continue_register, fields, email


def register_user(email, username, password, password_repeat, roles=None):
    """
    Registers a user if it complies with all the checks
    :param email: email address
    :param username: username to display
    :param password: password
    :param password_repeat: password repeated
    :param roles: user roles
    :return: status message. This one also specifies what action to take for the front-end, and also a user-readable
    error-message if applicable
    """
    if roles is None:
        roles = ['user']

    continue_register, fields, email = validate_register_fields(email, username, password, password_repeat)

    # If, and only if we don't have any invalid fields we actually register the user
    if any('false' in field.values() for field in fields.values()):
        continue_register = False

    if continue_register:
        # Hash password and register the user to the database
        user_datastore.create_user(email=email, username=username, password=hash_password(password), roles=roles)
        db.session.commit()
        return create_status(200, continue_register=continue_register, fields=fields)
    else:
        return create_status(400, continue_register=continue_register, fields=fields)

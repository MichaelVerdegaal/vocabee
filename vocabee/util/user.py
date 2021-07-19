import re

from email_validator import validate_email, EmailNotValidError
from flask_security import hash_password

from vocabee import user_datastore
from vocabee.util.view_util import create_status


def setup_roles(db):
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
    :return: field check report as dict, email (normalized if applicable)
    """

    def set_field_invalid(field, error):
        """Quick helper function for the fields, to lessen the amount of code"""
        fields[field]['valid'] = 'false'
        fields[field]['error'].append(error)

    fields = {field: {'valid': 'true', 'error': []} for field in ['email', 'username', 'password', 'password_repeat']}

    # Check for existing accounts
    if user_datastore.find_user(email=email):
        set_field_invalid('email', "An account with this email already exists")
    if user_datastore.find_user(username=username):
        set_field_invalid('username', "An account with this username already exists")

    ### Email field ###
    # Validate email and normalize
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e:
        set_field_invalid('email', f"{str(e)}")

    ### Username field ###
    if not username:
        set_field_invalid('username', "Username field can't be empty")
    if len(username) > 24:
        set_field_invalid('username', "Username is too long, please limit it to maximum 24 characters")
    # Only allow certain characters for the username, as a form of normalizing
    if not re.match("^[a-zA-Z0-9_.-]+$", username):
        set_field_invalid('username', "Username can only consist of letters, numbers and these special "
                                      "characters .-_ (period, dash and underline)")

    ### Password field ###
    if len(password) < 6:
        set_field_invalid('password', "Password is too short, please write a new one between 6-18 characters")
    elif len(password) > 18:
        set_field_invalid('password', "Password is too long, please write a new one between 6-18 characters")

    if password != password_repeat:
        set_field_invalid('password', "The passwords don't match")
        set_field_invalid('password_repeat', "The passwords don't match")

    return fields, email


def register_user(db, email, username, password, password_repeat, roles=None):
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

    fields, email = validate_register_fields(email, username, password, password_repeat)

    # If, and only if we don't have any invalid fields we actually register the user
    if any('false' in field.values() for field in fields.values()):
        return create_status(400, continue_register=False, fields=fields)
    else:
        # Hash password and register the user to the database
        user_datastore.create_user(email=email, username=username, password=hash_password(password), roles=roles)
        db.session.commit()
        return create_status(200, continue_register=True, fields=fields)

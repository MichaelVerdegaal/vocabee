from flask import Blueprint, render_template_string, render_template
from flask_security import auth_required, logout_user

from vocabee.queries.user import setup_test_users, setup_roles

user_bp = Blueprint('user', __name__, url_prefix='/user')
setup_roles()


# Views
@user_bp.route("/login")
@auth_required()
def login():
    setup_test_users()
    return render_template_string("Hello {{ current_user.email }}, with role {{ current_user.roles[0].name}}")


@user_bp.route("/logout")
@auth_required()
def logout():
    logout_user()
    return render_template('security/logout_user.html')

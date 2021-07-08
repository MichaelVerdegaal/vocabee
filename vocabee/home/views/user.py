from flask import Blueprint, render_template_string
from flask_security import auth_required

from vocabee.queries.user import setup_test_users, setup_roles

user_bp = Blueprint('user', __name__, url_prefix='/user')
setup_roles()


# Views
@user_bp.route("/hi")
@auth_required()
def home():
    setup_test_users()
    return render_template_string("Hello {{ current_user.email }}, with role {{ current_user.roles[0].name}}")

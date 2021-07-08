from flask import Blueprint, render_template_string
from flask_security import auth_required

from vocabee.queries.user import create_user

user_bp = Blueprint('user', __name__, url_prefix='/user')


# Views
@user_bp.route("/hi")
@auth_required()
def home():
    create_user()
    return render_template_string("Hello {{ current_user.email }}")

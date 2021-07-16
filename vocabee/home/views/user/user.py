from flask import Blueprint, render_template_string, render_template
from flask_security import auth_required, logout_user

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route("/login")
@auth_required()
def login():
    return render_template_string("Hello {{ current_user.email }}, with role {{ current_user.roles[0].name}}")


@user_bp.route("/logout")
@auth_required()
def logout():
    logout_user()
    return render_template('security/logout_user.html')


@user_bp.route("/register")
def register_page():
    return render_template("security/register_user.html")


@user_bp.route("/register-sucess")
def register_successful_page():
    return render_template("security/register_successful.html")

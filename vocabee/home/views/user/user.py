from flask import Blueprint, render_template, redirect, url_for
from flask_security import auth_required, logout_user, current_user

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route("/login")
@auth_required()
def login():
    return redirect(url_for('user.account'))


@user_bp.route("/logout")
@auth_required()
def logout():
    logout_user()
    return render_template('security/logout_user.html')


@user_bp.route("/register")
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    else:
        return render_template("security/register_user.html")


@user_bp.route("/register-sucess")
def register_successful_page():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    else:
        return render_template("security/register_successful.html")


@user_bp.route("/account")
@auth_required()
def account():
    return render_template('security/account.html')

from flask import Blueprint, request

from vocabee.util.user import register_user
from vocabee import db

user_ajax_bp = Blueprint('user_ajax', __name__, url_prefix='/user/ajax')


@user_ajax_bp.route('register', methods=['POST'])
def register():
    data = request.json
    status = register_user(db, data['email'], data['username'], data['password'], data['password_repeat'])
    return status, status['code']

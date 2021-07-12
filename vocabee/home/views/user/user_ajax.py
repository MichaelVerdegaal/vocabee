from flask import Blueprint, request

from vocabee.util.user import register_user

user_ajax_bp = Blueprint('user_ajax', __name__, url_prefix='/user/ajax')


@user_ajax_bp.route('register', methods=['POST'])
def register():
    data = request.json
    status = register_user(data['email'], data['username'], data['password'])
    return status, status['code']

from flask import Blueprint, request

from vocabee.util.view_util import create_status

user_ajax_bp = Blueprint('user_ajax', __name__, url_prefix='/user/ajax')


@user_ajax_bp.route('register', methods=['POST'])
def register():
    data = request.json
    print(data)
    return create_status(200), 200

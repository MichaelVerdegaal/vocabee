from flask import Blueprint, send_from_directory, request

miscellaneous_bp = Blueprint('miscellaneous', __name__, url_prefix='/misc', static_folder='../static')


@miscellaneous_bp.route('/robots.txt')
@miscellaneous_bp.route('/sitemap.xml')
def static_from_root():
    print(miscellaneous_bp.static_folder, request.path[6:])
    return send_from_directory(miscellaneous_bp.static_folder, request.path[6:])

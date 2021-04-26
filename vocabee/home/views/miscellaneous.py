from flask import Blueprint, send_from_directory, request

miscellaneous_bp = Blueprint('miscellaneous', __name__)


@miscellaneous_bp.route('/robots.txt')
@miscellaneous_bp.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(miscellaneous_bp.static_folder, request.path[1:])

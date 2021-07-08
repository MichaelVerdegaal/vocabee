from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from flask_security import roles_accepted, auth_required
from vocabee import cache

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/editor')
@cache.cached(timeout=30)
@auth_required()
@roles_accepted('admin', 'editor')
def editor():
    """
    Renders the editor page
    :return: Webpage
    """
    try:
        return render_template("admin/editor.html")
    except TemplateNotFound:
        abort(404)

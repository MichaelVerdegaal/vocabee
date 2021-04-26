from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from vocabee import cache

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/editor')
@cache.cached(timeout=30)
def editor():
    """
    Renders the editor page
    :return: Webpage
    """
    try:
        return render_template("admin/editor.html")
    except TemplateNotFound:
        abort(404)

from flask import Blueprint, request

from vocabee.util.queries import (get_example_by_id, get_examples_by_vocabulary_id, update_example, add_example,
                                  delete_example)
from vocabee.util.view_util import create_status

example_ajax_bp = Blueprint('example_ajax', __name__, url_prefix='/example/ajax')


@example_ajax_bp.route('/source/entry/get/<example_id>')
def example_entry_get(example_id):
    """
    AJAX endpoint to retrieve an example
    :param example_id: example id
    :return: example entry in JSON
    """
    status, entry = get_example_by_id(example_id)
    if entry:
        return entry.to_dict(), 200
    else:
        return status, status['code']


@example_ajax_bp.route('/source/entries/get/<vocabulary_id>')
def examples_get_by_vocabulary_id(vocabulary_id):
    """
    AJAX endpoint to retrieve multiple examples
    :param vocabulary_id: vocabulary id\
    :return: example entry in JSON
    """
    status, entries = get_examples_by_vocabulary_id(vocabulary_id)
    entries = {"entries": [e.to_dict() for e in entries]}
    if entries:
        return entries, 200
    else:
        return status, status['code']


@example_ajax_bp.route('/source/entry/update', methods=['POST'])
def example_entry_update():
    """
    AJAX endpoint to update an example entry
    :return: status
    """
    data = request.json
    if not data:
        return create_status(400, "Data received is empty"), 400
    status = update_example(data['id'], data['sentence_jp'], data['sentence_en'])
    if status['code'] == 200:
        return status, 200
    else:
        return status, 500


@example_ajax_bp.route('/source/entry/add', methods=['POST'])
def example_entry_add():
    """
    AJAX endpoint to add an example entry
    :return: status
    """
    data = request.json
    if not data:
        return create_status(400, "Data received is empty"), 400
    status = add_example(data['sentence_jp'], data['sentence_en'], data['vocab_id'])
    if status['code'] == 200:
        return status, 200
    else:
        return status, 500


@example_ajax_bp.route('/source/entry/delete', methods=['POST'])
def example_entry_delete():
    """
    AJAX endpoint to add an example entry
    :return: status
    """
    data = request.json
    if not data:
        return create_status(400, "Data received is empty"), 400
    status = delete_example(data['id'])
    if status['code'] == 200:
        return status, 200
    else:
        return status, 500

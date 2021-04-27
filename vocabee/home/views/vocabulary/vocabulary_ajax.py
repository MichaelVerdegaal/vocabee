import os
from pathlib import Path

from flask import Blueprint, request, Response

from vocabee.util.anki_util import create_deck_by_level
from vocabee.util.queries import get_vocab_by_level, get_vocab_by_id, update_vocab, add_vocab, delete_vocab
from vocabee.util.vocabulary_util import process_vocabulary
from vocabee import project_folder
vocabulary_ajax_bp = Blueprint('vocabulary_ajax', __name__, url_prefix='/vocabulary/ajax')


@vocabulary_ajax_bp.route('/source/<int:vocab_level>')
def vocabulary_full_get(vocab_level):
    """
    AJAX endpoint to retrieve vocabulary
    :param vocab_level: Valid JLPT vocabulary level (1-5)
    :return: vocabulary in JSON
    """
    if 0 < vocab_level < 6:
        vocab = process_vocabulary(get_vocab_by_level(vocab_level))
        return vocab
    else:
        "Faulty vocabulary level"


@vocabulary_ajax_bp.route('/source/entry/get/<int:vocab_id>')
def vocabulary_entry_get(vocab_id):
    """/vocab
    AJAX endpoint to retrieve vocabulary
    :param vocab_id: vocabulary id
    :return: vocabulary entry in JSON
    """
    entry = get_vocab_by_id(vocab_id)
    return entry.to_dict() if entry else ""


@vocabulary_ajax_bp.route('/source/entry/update', methods=['POST'])
def vocabulary_entry_update():
    """
    AJAX endpoint to update a vocabulary entry
    :return: status
    """
    data = dict(request.form)
    update_vocab(data['id'], data['kanji'], data['kana'], data['meaning'], data['jlpt_level'])
    print(f"Updated vocabulary entry {data['id']}")
    return {'status': 'success'}


@vocabulary_ajax_bp.route('/source/entry/add', methods=['POST'])
def vocabulary_entry_add():
    """
    AJAX endpoint to add a vocabulary entry
    :return: status
    """
    data = dict(request.form)
    add_vocab(data['kanji'], data['kana'], data['meaning'], data['jlpt_level'])
    print("Added new vocabulary entry")
    return {'status': 'success'}


@vocabulary_ajax_bp.route('/source/entry/delete', methods=['POST'])
def vocabulary_entry_delete():
    """
    AJAX endpoint to add a vocabulary entry
    :return: status
    """
    data = dict(request.form)
    delete_vocab(data['id'])
    print(f"Deleted vocabulary entry {data['id']}")
    return {'status': 'success'}


@vocabulary_ajax_bp.route('/source/anki/<int:vocab_level>')
def vocabulary_download_deck(vocab_level):
    """
    Creates download response for generated anki decks
    :param vocab_level: Valid JLPT vocabulary level (1-5)
    :return: downloaded file
    """

    vocab = get_vocab_by_level(vocab_level)
    # TODO make a proper constant for the static folder
    project_root = Path(vocabulary_ajax_bp.root_path).parents[3]
    filename = f'vocabee{vocab_level}.apkg'
    print(project_folder, project_root)
    path = os.path.join(project_root, filename)
    create_deck_by_level(vocab, vocab_level, filename)

    # Ref: https://stackoverflow.com/a/57998006/7174982
    with open(path, 'rb') as f:
        data = f.readlines()
    os.remove(path)
    return Response(data, headers={
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': 'attachment; filename=%s;' % filename
    })

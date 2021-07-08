import os

from flask import Blueprint, request, Response

from vocabee.config import PROJECT_FOLDER
from vocabee.util.anki_util import create_deck_by_level
from vocabee.queries.vocabulary import (get_vocabulary_by_level, get_all_vocabulary_no_examples,
                                        get_vocabulary_by_level_no_examples, get_vocabulary_by_id, update_vocab,
                                        add_vocab, delete_vocab)
from vocabee.util.view_util import create_status
from vocabee.util.vocabulary_util import process_vocabulary, search_vocabulary
from time import perf_counter

vocabulary_ajax_bp = Blueprint('vocabulary_ajax', __name__, url_prefix='/vocabulary/ajax')


@vocabulary_ajax_bp.route('/source/search/<string:search_query>')
def vocabulary_full_search(search_query):
    """
    AJAX endpoint to retrieve vocabulary
    :return: vocabulary in JSON
    """
    status, vocabulary = get_all_vocabulary_no_examples()
    if status['code'] == 200:
        start_time = perf_counter()
        vocabulary_dict = {'entries': [dict(row) for row in vocabulary]}
        results = search_vocabulary(search_query, vocabulary_dict)
        end_time = perf_counter()
        search_time = f"{end_time - start_time:.5f}"
        results['search_time'] = search_time
        if (results['perfect_match_count'] + results['match_count']) == 0:
            return create_status(404, "No matches found"), 404
        else:
            return results, 200
    else:
        return status, 500


@vocabulary_ajax_bp.route('/source/<int:vocabulary_level>')
def vocabulary_full_get_by_level(vocabulary_level):
    """
    AJAX endpoint to retrieve vocabulary
    :param vocabulary_level: Valid JLPT vocabulary level (1-5)
    :return: vocabulary in JSON
    """
    if 0 < vocabulary_level < 6:
        status, vocabulary = get_vocabulary_by_level_no_examples(vocabulary_level)
        if status['code'] == 200:
            vocabulary = process_vocabulary(vocabulary)
            return vocabulary, 200
        else:
            return status, 500
    else:
        return create_status(400, "Faulty vocabulary level"), 400


@vocabulary_ajax_bp.route('/source/entry/get/<int:vocabulary_id>')
def vocabulary_entry_get(vocabulary_id):
    """
    AJAX endpoint to retrieve vocabulary
    :param vocabulary_id: vocabulary id
    :return: vocabulary entry in JSON
    """
    status, entry = get_vocabulary_by_id(vocabulary_id)
    if entry:
        return entry.to_dict(), 200
    else:
        return status, status['code']


@vocabulary_ajax_bp.route('/source/entry/update', methods=['POST'])
def vocabulary_entry_update():
    """
    AJAX endpoint to update a vocabulary entry
    :return: status
    """
    data = request.json
    if not data:
        return create_status(400, "Data received is empty"), 400
    status = update_vocab(data['id'], data['kanji'], data['kana'], data['meaning'], data['jlpt_level'])
    if status['code'] == 200:
        return status, 200
    else:
        return status, 500


@vocabulary_ajax_bp.route('/source/entry/add', methods=['POST'])
def vocabulary_entry_add():
    """
    AJAX endpoint to add a vocabulary entry
    :return: status
    """
    data = request.json
    if not data:
        return create_status(400, "Data received is empty"), 400
    status = add_vocab(data['kanji'], data['kana'], data['meaning'], data['jlpt_level'])
    if status['code'] == 200:
        return status, 200
    else:
        return status, 500


@vocabulary_ajax_bp.route('/source/entry/delete', methods=['POST'])
def vocabulary_entry_delete():
    """
    AJAX endpoint to add a vocabulary entry
    :return: status
    """
    data = request.json
    if not data:
        return create_status(400, "Data received is empty"), 400
    status = delete_vocab(data['id'])
    if status['code'] == 200:
        return status, 200
    else:
        return status, 500


@vocabulary_ajax_bp.route('/source/anki/<int:vocabulary_level>')
def vocabulary_download_deck(vocabulary_level):
    """
    Creates download response for generated anki decks
    :param vocabulary_level: Valid JLPT vocabulary level (1-5)
    :return: downloaded file
    """
    status, vocabulary = get_vocabulary_by_level(vocabulary_level)
    if status['code'] == 200:
        filename = f'vocabee{vocabulary_level}.apkg'
        deck_path = os.path.join(PROJECT_FOLDER, filename)
        create_deck_by_level(vocabulary, vocabulary_level, filename)

        # Ref: https://stackoverflow.com/a/57998006/7174982
        with open(deck_path, 'rb') as f:
            data = f.readlines()
        os.remove(deck_path)
        return Response(data, headers={'Content-Type': 'application/octet-stream',
                                       'Content-Disposition': f'attachment; filename={filename};'}), 200
    else:
        return status, 500

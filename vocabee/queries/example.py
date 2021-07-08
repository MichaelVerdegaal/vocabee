from sqlalchemy.exc import SQLAlchemyError

from vocabee import db
from vocabee.home.models import Example
from vocabee.util.view_util import create_status


def get_example_by_id(example_id):
    """
    Fetches example entry by id
    :param example_id: Example ID
    :return: Queryset
    """
    try:
        entry = Example.query.filter_by(id=example_id).one_or_none()
        if entry:
            return create_status(), entry
        else:
            return create_status(404), None
    except SQLAlchemyError as e:
        return create_status(500, repr(e)), None


def get_examples_by_vocabulary_id(vocabulary_id):
    """
    Fetches multiple examples by vocabulary id
    :param vocabulary_id: vocabulary id
    :return: Queryset
    """
    try:
        examples = Example.query.filter_by(vocab_id=vocabulary_id).all()
        if examples:
            return create_status(), examples
        else:
            return create_status(404), None
    except SQLAlchemyError as e:
        return create_status(500, repr(e)), None


def update_example(example_id, sentence_jp, sentence_en):
    """
    Updates an example entry
    :param example_id: example ID
    :param sentence_jp: japanese sentence
    :param sentence_en: english sentence
    """
    try:
        Example.query.filter_by(id=example_id).update(dict(sentence_jp=sentence_jp, sentence_en=sentence_en))
        db.session.commit()
        return create_status()
    except SQLAlchemyError as e:
        return create_status(500, repr(e))


def add_example(sentence_jp, sentence_en, vocabulary_id):
    """
    Adds an example entry
    :param sentence_jp: japanese sentence
    :param sentence_en: english sentence
    :param vocabulary_id: Vocabulary ID
    """
    try:
        entry = Example(sentence_en=sentence_en, sentence_jp=sentence_jp, vocab_id=vocabulary_id)
        db.session.add(entry)
        db.session.commit()
        return create_status(example_id=entry.id)
    except SQLAlchemyError as e:
        return create_status(500, repr(e))


def delete_example(example_id):
    """
    Deletes an example entry
    :param example_id: Example entry
    """
    try:
        Example.query.filter_by(id=example_id).delete()
        db.session.commit()
        return create_status()
    except SQLAlchemyError as e:
        return create_status(500, repr(e))

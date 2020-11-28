import json

from vocabee.home.models import Vocabulary, Example
from vocabee.db_util import engine
from flask import current_app as app


def get_vocab_by_level(jlpt_level):
    """
    Fetches vocabulary entries by JLPT level
    :param jlpt_level: Vocabulary level
    :return: Queryset
    """
    vocabulary = app.session.query(Vocabulary).filter_by(jlpt_level=f"N{jlpt_level}").all()
    return vocabulary


def get_examples_by_id(vocab_id):
    """
    Retrieves example sentences based on the vocabulary id they're linked to
    :param vocab_id: vocabulary entry id
    :return: examples as an multidimensional array
    """
    examples = Example.query.filter_by(vocab_id=vocab_id).all()
    return examples


def serialize_examples(examples):
    """
    Serialize example queryset to json
    :param examples: example entries
    :return: json
    """
    return json.dumps(Example.serialize_list(examples))


def call_create_temp_example_samples(vocab_level):
    app.session.execute(f"CALL create_temp_example_samples('example_sample_lvl_{vocab_level}', 'N{vocab_level}')")
    app.session.commit()


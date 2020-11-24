import json

from flask_sqlalchemy_caching import FromCache

from vocabee import cache
from vocabee.home.models import Vocabulary, Example


def get_all_vocab():
    """
    Fetches all vocabulary entries from the database
    :return: vocabulary
    """
    return Vocabulary.query.options(FromCache(cache)).all()


def get_vocab_by_level(jlpt_level):
    """
    Fetches vocabulary entries by JLPT level
    :param jlpt_level: Vocabulary level
    :return: Queryset
    """
    vocabulary = Vocabulary.query.options(FromCache(cache)).filter_by(jlpt_level=f"N{jlpt_level}").all()
    return vocabulary


def get_examples_by_id(vocab_id):
    """
    Retrieves example sentences based on the vocabulary id they're linked to
    :param vocab_id: vocabulary entry id
    :return: examples as an multidimensional array
    """
    examples = Example.query.options(FromCache(cache)).filter_by(vocab_id=vocab_id).all()
    return examples


def serialize_examples(examples):
    """
    Serialize example queryset to json
    :param examples: example entries
    :return: json
    """
    return json.dumps(Example.serialize_list(examples))


def get_example_sample(vocab_id):
    """
    Retrieves examples linked to a vocabulary entry and randomly samples a few
    :param vocab_id: vocabulary id
    :return: a list of up to 3 examples
    """
    examples = (Example.query
                .options(FromCache(cache))
                .with_entities(Example.sentence_jp, Example.sentence_en)
                .filter_by(vocab_id=vocab_id)
                .limit(3)
                .all())
    return examples

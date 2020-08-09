import json

from vocabee.home.models import Vocabulary, Example


def get_all_vocab():
    """
    Fetches all vocabulary entries from the database
    :return: vocabulary
    """
    return Vocabulary.query.all()


def get_vocab_by_level(jlpt_level):
    """
    Fetches vocabulary entries by JLPT level
    :param jlpt_level: Vocabulary level
    :return: Queryset
    """
    vocabulary = Vocabulary.query.filter_by(jlpt_level=f"N{jlpt_level}").all()
    return vocabulary


def get_examples_by_id(vocab_id):
    """
    Retrieves example sentences based on the vocabulary id they're linked to
    :param vocab_id: vocabulary entry id
    :return: examples as an multidimensional array
    """
    examples = Example.query.filter_by(vocab_id=vocab_id).all()
    examples = json.dumps(Example.serialize_list(examples))
    return examples

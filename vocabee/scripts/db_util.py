import json

from vocabee.scripts.models import Vocabulary, Example


def get_all_vocab():
    """
    Fetches all vocabulary entries from the database
    :param cursor: cursor object
    :return: vocabulary
    """
    return Vocabulary.query.all()


def get_examples_by_id(vocab_id):
    """
    Retrieves example sentences based on the vocabulary id they're linked to
    :param cursor: cursor object
    :param vocab_id: vocabulary entry id
    :return: examples as valid json
    """
    examples = Example.query.filter_by(vocab_id=vocab_id).all()
    examples = json.dumps(Example.serialize_list(examples))
    print(examples)
    return examples

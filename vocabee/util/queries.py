from vocabee import cache
from vocabee.home.models import Vocabulary


@cache.memoize(300)
def get_vocab_by_level(jlpt_level):
    """
    Fetches vocabulary entries by JLPT level
    :param jlpt_level: Vocabulary level
    :return: Queryset
    """
    vocabulary = Vocabulary.query.filter_by(jlpt_level=f"N{jlpt_level}").all()
    return vocabulary


@cache.memoize(60)
def get_vocab_by_id(vocab_id):
    """
    Fetches vocabulary entry by id
    :param vocab_id: Vocabulary ID
    :return: Queryset
    """
    entry = Vocabulary.query.filter_by(id=vocab_id).one_or_none()
    return entry


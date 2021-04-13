from vocabee import cache
from vocabee.home.models import Vocabulary, db


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


def update_vocab(vocab_id, kanji, kana, meaning, jlpt_level):
    """
    Updates a vocabulary entry
    :param vocab_id: vocabulary entry
    :param kanji: kanji field
    :param kana: kana field
    :param meaning: meaning field
    :param jlpt_level: jlpt_level field
    """
    Vocabulary.query.filter_by(id=vocab_id).update(dict(kanji=kanji,
                                                        hiragana=kana,
                                                        english=meaning,
                                                        jlpt_level=jlpt_level))
    db.session.commit()


def add_vocab(kanji, kana, meaning, jlpt_level):
    """
    Adds a vocabulary entry
    :param kanji: kanji field
    :param kana: kana field
    :param meaning: meaning field
    :param jlpt_level: jlpt_level field
    """
    entry = Vocabulary(kanji=kanji,
                       hiragana=kana,
                       english=meaning,
                       jlpt_level=jlpt_level)
    db.session.add(entry)
    db.session.commit()


def delete_vocab(vocab_id):
    """
    Deletes a vocabulary entry
    :param vocab_id: vocabulary entry
    """
    Vocabulary.query.filter_by(id=vocab_id).delete()
    db.session.commit()

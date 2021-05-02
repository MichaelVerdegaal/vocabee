from vocabee import cache
from vocabee.home.models import Vocabulary, db
from sqlalchemy.exc import SQLAlchemyError
from vocabee.util.view_util import create_status


@cache.memoize(300)
def get_vocab_by_level(jlpt_level):
    """
    Fetches vocabulary entries by JLPT level
    :param jlpt_level: Vocabulary level
    :return: Queryset
    """
    try:
        vocabulary = Vocabulary.query.filter_by(jlpt_level=f"N{jlpt_level}").all()
        return create_status(), vocabulary
    except SQLAlchemyError as e:
        return create_status(500, str(e)), None


@cache.memoize(5)
def get_vocab_by_id(vocab_id):
    """
    Fetches vocabulary entry by id
    :param vocab_id: Vocabulary ID
    :return: Queryset
    """
    try:
        entry = Vocabulary.query.filter_by(id=vocab_id).one_or_none()
        if entry:
            return create_status(), entry
        else:
            return create_status(404), None
    except SQLAlchemyError as e:
        return create_status(500, str(e)), None


def update_vocab(vocab_id, kanji, kana, meaning, jlpt_level):
    """
    Updates a vocabulary entry
    :param vocab_id: vocabulary entry
    :param kanji: kanji field
    :param kana: kana field
    :param meaning: meaning field
    :param jlpt_level: jlpt_level field
    """
    try:
        Vocabulary.query.filter_by(id=vocab_id).update(dict(kanji=kanji,
                                                            hiragana=kana,
                                                            english=meaning,
                                                            jlpt_level=jlpt_level))
        db.session.commit()
        return create_status()
    except SQLAlchemyError as e:
        return create_status(500, str(e))


def add_vocab(kanji, kana, meaning, jlpt_level):
    """
    Adds a vocabulary entry
    :param kanji: kanji field
    :param kana: kana field
    :param meaning: meaning field
    :param jlpt_level: jlpt_level field
    """
    try:
        entry = Vocabulary(kanji=kanji,
                           hiragana=kana,
                           english=meaning,
                           jlpt_level=jlpt_level)
        db.session.add(entry)
        db.session.commit()
        return create_status(vocab_id=entry.id)
    except SQLAlchemyError as e:
        return create_status(500, str(e))


def delete_vocab(vocab_id):
    """
    Deletes a vocabulary entry
    :param vocab_id: vocabulary entry
    """
    try:
        Vocabulary.query.filter_by(id=vocab_id).delete()
        db.session.commit()
        return create_status()
    except SQLAlchemyError as e:
        return create_status(500, str(e))

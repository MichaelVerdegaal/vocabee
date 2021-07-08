from sqlalchemy.exc import SQLAlchemyError

from vocabee import cache, db
from vocabee.home.models import Vocabulary
from vocabee.util.view_util import create_status


@cache.memoize(300)
def get_vocabulary_by_level(jlpt_level):
    """
    Fetches vocabulary entries by JLPT level
    :param jlpt_level: Vocabulary level
    :return: Queryset
    """
    try:
        vocabulary = Vocabulary.query.filter_by(jlpt_level=f"N{jlpt_level}").all()
        return create_status(), vocabulary
    except SQLAlchemyError as e:
        return create_status(500, repr(e)), None


@cache.memoize(300)
def get_all_vocabulary_no_examples():
    """
    Fetches vocabulary entries by JLPT level, but only includes necessary columns to increase performance
    :return: Queryset
    """
    try:
        vocabulary = Vocabulary.query.with_entities(Vocabulary.id,
                                                    Vocabulary.kanji,
                                                    Vocabulary.kana,
                                                    Vocabulary.english,
                                                    Vocabulary.jlpt_level).all()
        return create_status(), vocabulary
    except SQLAlchemyError as e:
        return create_status(500, repr(e)), None


@cache.memoize(300)
def get_vocabulary_by_level_no_examples(jlpt_level):
    """
    Fetches vocabulary entries by JLPT level, but only includes necessary columns to increase performance
    :param jlpt_level: Vocabulary level
    :return: Queryset
    """
    try:
        vocabulary = Vocabulary.query.filter_by(jlpt_level=f"N{jlpt_level}").with_entities(Vocabulary.id,
                                                                                           Vocabulary.kanji,
                                                                                           Vocabulary.kana,
                                                                                           Vocabulary.english).all()
        return create_status(), vocabulary
    except SQLAlchemyError as e:
        return create_status(500, repr(e)), None


@cache.memoize(5)
def get_vocabulary_by_id(vocabulary_id):
    """
    Fetches vocabulary entry by id
    :param vocabulary_id: Vocabulary ID
    :return: Queryset
    """
    try:
        entry = Vocabulary.query.filter_by(id=vocabulary_id).one_or_none()
        if entry:
            return create_status(), entry
        else:
            return create_status(404), None
    except SQLAlchemyError as e:
        return create_status(500, repr(e)), None


def update_vocab(vocabulary_id, kanji, kana, meaning, jlpt_level):
    """
    Updates a vocabulary entry
    :param vocabulary_id: vocabulary id
    :param kanji: kanji field
    :param kana: kana field
    :param meaning: meaning field
    :param jlpt_level: jlpt_level field
    """
    try:
        Vocabulary.query.filter_by(id=vocabulary_id).update(dict(kanji=kanji,
                                                                 kana=kana,
                                                                 english=meaning,
                                                                 jlpt_level=jlpt_level))
        db.session.commit()
        return create_status()
    except SQLAlchemyError as e:
        return create_status(500, repr(e))


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
                           kana=kana,
                           english=meaning,
                           jlpt_level=jlpt_level)
        db.session.add(entry)
        db.session.commit()
        return create_status(vocabulary_id=entry.id)
    except SQLAlchemyError as e:
        return create_status(500, repr(e))


def delete_vocab(vocabulary_id):
    """
    Deletes a vocabulary entry
    :param vocabulary_id: vocabulary entry
    """
    try:
        Vocabulary.query.filter_by(id=vocabulary_id).delete()
        db.session.commit()
        return create_status()
    except SQLAlchemyError as e:
        return create_status(500, repr(e))

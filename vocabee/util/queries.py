from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from vocabee import cache
from vocabee.home.models import Vocabulary, Example, db
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


@cache.memoize(300)
def get_vocab_range(jlpt_level, table_start, table_length):
    """
    Fetches vocabulary entries by JLPT level
    :param jlpt_level: Vocabulary level
    :return: Queryset
    """
    try:
        # TODO: switch to the window function once we're at MySQL 8. This is what i originally planned to use,
        #  but Pythonanywhere is still stuck on 5.7
        # # Ref: https://stackoverflow.com/questions/38160213/filter-by-row-number-in-sqlalchemy
        # row_number_column = func.row_number().over(partition_by=Vocabulary.id,
        #                                            order_by=Vocabulary.id).label('row_number')
        # vocabulary = Vocabulary.query
        # vocabulary = vocabulary.filter_by(jlpt_level=f"N{jlpt_level}")
        # vocabulary = vocabulary.add_column(row_number_column)
        # vocabulary = vocabulary.filter(row_number_column == table_start)
        # vocabulary = vocabulary.limit(table_length)
        # vocabulary = vocabulary.all()
        query = text("""
        SELECT c.*
        FROM   (SELECT ( @row_number := @row_number + 1 ) AS row_num,
                        id,
                        kanji,
                        hiragana,
                        english
                FROM   vocabulary WHERE jlpt_level = :level) AS c
        LIMIT  :tstart, :tlen;
        """)
        db.session.execute(text("SET @row_number = 0;"))
        vocabulary = db.session.execute(query, {'level': f"N{jlpt_level}", 'tstart': table_start, 'tlen': table_length})
        voc_list = [dict(i) for i in vocabulary]
        return create_status(), voc_list
    except SQLAlchemyError as e:
        print(e)
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
        return create_status(500, str(e)), None


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
        return create_status(500, str(e))


def add_example(sentence_jp, sentence_en, vocab_id):
    """
    Adds an example entry
    :param sentence_jp: japanese sentence
    :param sentence_en: english sentence
    :param vocab_id: Vocabulary ID
    """
    try:
        entry = Example(sentence_en=sentence_en, sentence_jp=sentence_jp, vocab_id=vocab_id)
        db.session.add(entry)
        db.session.commit()
        return create_status(example_id=entry.id)
    except SQLAlchemyError as e:
        return create_status(500, str(e))


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
        return create_status(500, str(e))

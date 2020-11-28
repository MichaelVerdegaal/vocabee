from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship

from vocabee.db_util import Base

column = Column
string = String
integer = Integer
foreign_key = ForeignKey


class Vocabulary(Base, SerializerMixin):
    __tablename__ = 'vocabulary'
    serialize_rules = ('-examples.vocabulary',)

    id = column(integer, primary_key=True)
    kanji = column(string(), nullable=True)
    hiragana = column(string(), nullable=False)
    english = column(string(), nullable=False)
    jlpt_level = column(string(), nullable=False)
    examples = relationship("Example", backref="vocabulary", lazy="joined")

    # TODO: create an universal tostring method
    def __str__(self):
        return (f'ID: [{self.id}],'
                f' Kanji: [{self.kanji}],'
                f' Hiragana: [{self.hiragana}],'
                f' English: [{self.english}],'
                f' JLPT level: [{self.jlpt_level}]')


class Example(Base, SerializerMixin):
    __tablename__ = 'example'
    id = column(integer, primary_key=True)
    sentence_jp = column(string())
    sentence_en = column(string())
    vocab_id = column(integer, foreign_key('vocabulary.id'))

    def __str__(self):
        return f'ID: [{self.id}], Sentence EN: [{self.sentence_en}], Sentence JP: [{self.sentence_jp}]'

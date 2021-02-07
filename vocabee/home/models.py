from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from vocabee import db

column = Column
string = String
integer = Integer
foreign_key = ForeignKey
model = db.Model


class Vocabulary(model, SerializerMixin):
    __tablename__ = 'vocabulary'
    serialize_rules = ('-examples.vocabulary',)

    id = column(integer, primary_key=True)
    kanji = column(string(100), nullable=True)
    hiragana = column(string(300), nullable=False)
    english = column(string(300), nullable=False)
    jlpt_level = column(string(5), nullable=False)
    examples = relationship("Example", backref="vocabulary", lazy="joined")

    # TODO: create an universal tostring method
    def __str__(self):
        return (f'ID: [{self.id}],'
                f' Kanji: [{self.kanji}],'
                f' Hiragana: [{self.hiragana}],'
                f' English: [{self.english}],'
                f' JLPT level: [{self.jlpt_level}]')


class Example(model, SerializerMixin):
    __tablename__ = 'example'
    id = column(integer, primary_key=True)
    sentence_jp = column(string(500))
    sentence_en = column(string(500))
    vocab_id = column(integer, foreign_key('vocabulary.id'))

    def __str__(self):
        return f'ID: [{self.id}], Sentence EN: [{self.sentence_en}], Sentence JP: [{self.sentence_jp}]'

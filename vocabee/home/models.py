from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from vocabee import db

column = Column
string = String
integer = Integer
foreign_key = ForeignKey
model = db.Model


def tostr(cls):
    """
    Decorator function to create a str representation for an object
    :param cls: The class to be passed to the function
    :return: The updated class
    """

    def __str__(self):
        obj_name = type(self).__name__
        attr = ', '.join('{}: [{}]'.format(*item) for item in vars(self).items())
        return f'{obj_name}({attr})'

    cls.__str__ = __str__
    cls.__repr__ = __str__
    return cls


@tostr
class Vocabulary(model, SerializerMixin):
    __tablename__ = 'vocabulary'
    serialize_rules = ('-examples.vocabulary',)

    id = column(integer, primary_key=True)
    kanji = column(string(100), nullable=True)
    hiragana = column(string(300), nullable=False)
    english = column(string(300), nullable=False)
    jlpt_level = column(string(5), nullable=False)
    examples = relationship("Example", backref="vocabulary", lazy="joined")


@tostr
class Example(model, SerializerMixin):
    __tablename__ = 'example'
    id = column(integer, primary_key=True)
    sentence_jp = column(string(500))
    sentence_en = column(string(500))
    vocab_id = column(integer, foreign_key('vocabulary.id'))

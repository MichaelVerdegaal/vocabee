from sqlalchemy.inspection import inspect

from vocabee.scripts.main import db

column = db.Column
string = db.String
integer = db.Integer
foreign_key = db.ForeignKey


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(model_list):
        return [model.serialize() for model in model_list]


class Vocabulary(db.Model, Serializer):
    __tablename__ = 'vocabulary'
    id = column(integer, primary_key=True)
    kanji = column(string(), nullable=True)
    hiragana = column(string(), nullable=False)
    english = column(string(), nullable=False)
    jlpt_level = column(string(), nullable=False)


class Example(db.Model, Serializer):
    __tablename__ = 'example'
    id = column(integer, primary_key=True)
    sentence_jp = column(string())
    sentence_en = column(string())
    vocab_id = column(integer, foreign_key('vocabulary.id'))

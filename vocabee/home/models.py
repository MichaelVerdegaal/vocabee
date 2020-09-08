from sqlalchemy.inspection import inspect

from vocabee import db

column = db.Column
string = db.String
integer = db.Integer
foreign_key = db.ForeignKey
model = db.Model


class Serializer(object):
    """
    Helper class to assist model objects to be used in the front-end
    """

    def serialize(self):
        """
        Serialize a model object to a dictionary
        :return: Serialized object
        """
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    def to_list(self):
        """
        Serialize a model object to a list
        :return: Serialized object
        """
        return [getattr(self, c) for c in inspect(self).attrs.keys()]

    @staticmethod
    def serialize_list(model_list, use_list=True):
        """
        Serialize multiple model objects to a dictionary or list
        :param model_list: model objects to serialize
        :param use_list: ff true it'll serialize the objects to a list, otherwise a dictionary
        :return: Serialized objects
        """
        if use_list:
            return [model.to_list() for model in model_list]
        else:
            return [model.serialize() for model in model_list]


class Vocabulary(model, Serializer):
    __tablename__ = 'vocabulary'
    id = column(integer, primary_key=True)
    kanji = column(string(), nullable=True)
    hiragana = column(string(), nullable=False)
    english = column(string(), nullable=False)
    jlpt_level = column(string(), nullable=False)

    # TODO: create an universal tostring method
    def __str__(self):
        return (f'ID: [{self.id}],'
                f' Kanji: [{self.kanji}],'
                f' Hiragana: [{self.hiragana}],'
                f' English: [{self.english}],'
                f' JLPT level: [{self.jlpt_level}]')


class Example(model, Serializer):
    __tablename__ = 'example'
    id = column(integer, primary_key=True)
    sentence_jp = column(string())
    sentence_en = column(string())
    vocab_id = column(integer, foreign_key('vocabulary.id'))

    def __str__(self):
        return f'ID: [{self.id}], Sentence EN: [{self.sentence_en}], Sentence JP: [{self.sentence_jp}]'

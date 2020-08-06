from vocabee.scripts.main import db

column = db.Column
string = db.String
integer = db.Integer
foreign_key = db.ForeignKey


class Vocabulary(db.Model):
    __tablename__ = 'vocabulary'
    id = column(integer, primary_key=True)
    kanji = column(string(), nullable=True)
    hiragana = column(string(), nullable=False)
    english = column(string(), nullable=False)
    jlpt_level = column(string(), nullable=False)


class Example(db.Model):
    __tablename__ = 'example'
    id = column(integer, primary_key=True)
    sentence_jp = column(string())
    sentence_en = column(string())
    vocab_id = column(integer, foreign_key('vocabulary.id'))

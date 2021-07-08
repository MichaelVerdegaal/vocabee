from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy_serializer import SerializerMixin

from vocabee import db


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
class Vocabulary(db.Model, SerializerMixin):
    """
    Table that holds vocabulary entries
    """
    __tablename__ = 'vocabulary'
    serialize_rules = ('-examples.vocabulary',)

    id = Column(Integer, primary_key=True)
    kanji = Column(String(100), nullable=True)
    kana = Column(String(300), nullable=False)
    english = Column(String(300), nullable=False)
    jlpt_level = Column(String(5), nullable=False)
    examples = relationship("Example", backref="vocabulary", lazy="dynamic")


@tostr
class Example(db.Model, SerializerMixin):
    """
    Table that holds example sentence entries, connected to a vocabulary entry
    """
    __tablename__ = 'example'
    id = Column(Integer, primary_key=True)
    sentence_jp = Column(String(500))
    sentence_en = Column(String(500))
    vocab_id = Column(Integer, ForeignKey('vocabulary.id'))


@tostr
class Role(db.Model, RoleMixin):
    """
    Table that holds user roles
    """
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(String(255))


@tostr
class User(db.Model, UserMixin):
    """
    Table that holds user accounts
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

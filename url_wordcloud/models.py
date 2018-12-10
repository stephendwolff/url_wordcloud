# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Text
from tornado_sqlalchemy import declarative_base

DeclarativeBase = declarative_base()


class Word(DeclarativeBase):
    """
    Word model
    pk: is salted hash of the word (so it can be compared, but not read in the plain)
    word: stored encrypted, with a key generated at start up, which can be read by a private key
    frequency: number of instances of word found
    """
    __tablename__ = 'words'

    pk = Column(String(255), primary_key=True)
    word = Column(Text)
    frequency = Column(Integer)

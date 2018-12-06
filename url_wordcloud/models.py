# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer
from tornado_sqlalchemy import declarative_base

DeclarativeBase = declarative_base()


class Word(DeclarativeBase):
    __tablename__ = 'words'

    pk = Column(String(100), primary_key=True)
    word = Column(String(255))
    frequency = Column(Integer)

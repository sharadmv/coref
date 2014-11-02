import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean

Base = declarative_base()

engine = create_engine("mysql://coref@localhost/coref")

class Question(Base):
    __tablename__ = "questions"
    qid = Column("qid", Integer, primary_key=True)
    question = Column("question", Text, nullable=False)

class Answer(Base):
    __tablename__ = "answers"
    aid = Column("aid", Integer, primary_key=True)
    qid = Column("qid", Integer, nullable=False)
    answer = Column("answer", Text, nullable=False)

class Coref(Base):
    __tablename__ = "coreferences"
    cid = Column("cid", Integer, primary_key=True)
    qid = Column("qid", Integer, nullable=False)
    pos_start = Column("pos_start", Integer, nullable=False)
    pos_end = Column("pos_end", Integer, nullable=False)
    description = Column("description", Text, nullable=False)
    coref_group = Column("coref_group", Integer, nullable=False)
    author = Column("author", String, nullable=False)
    date_added = Column("date_added", DateTime, default=datetime.datetime.utcnow(), nullable=False)

class User(Base):
    __tablename__ = "users"
    uid = Column("uid", Integer, primary_key=True)
    username = Column("username", String, nullable=False)
    password = Column("password", String, nullable=False)
    firstname = Column("firstname", String, nullable=False)
    lastname = Column("lastname", String, nullable=False)
    email = Column("email", String, nullable=False)
    last_qid = Column("last_qid", Integer, nullable=False)
    last_login = Column("las", Integer, nullable=False)
    last_login = Column("last_login", DateTime, nullable=False)
    is_admin = Column("is_admin", Boolean, nullable=False)

class UserHistory(Base):
    __tablename__ = "user_history"
    uhid = Column("uhid", Integer, primary_key=True)
    uid = Column("uid", Integer, nullable=False)
    qid = Column("qid", Integer, nullable=False)
    position = Column("position", Integer, nullable=False)

class Mention(Base):
    __tablename__ = "mentions"
    mid = Column("mid", Integer, primary_key=True)
    qid = Column("qid", Integer)
    pos_start = Column("pos_start", Integer)
    pos_end = Column("pos_end", Integer)

class QuestionOrder(Base):
    __tablename__ = "question_order"

Base.metadata.create_all(engine)

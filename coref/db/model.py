import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, UniqueConstraint, or_, Float
from sqlalchemy.orm import relationship

Base = declarative_base()

engine = create_engine("mysql://coref@localhost/coref")

class Question(Base):
    __tablename__ = "question"
    question_id = Column("question_id", Integer, primary_key=True)
    question = Column("question", Text, nullable=False)
    mention_pairs = relationship("MentionPair", backref="question")
    score = Column("score", Float)

    def corefs(self, session):
        return session.query(Coref).filter(Coref.question_id == self.question_id)

    def to_dict(self):
        return {
            'question_id': self.question_id,
            'text': self.question
        }

class Answer(Base):
    __tablename__ = "answer"
    answer_id = Column("answer_id", Integer, primary_key=True)
    question_id = Column("question_id", Integer, ForeignKey("question.question_id"), nullable=False)
    answer = Column("answer", Text, nullable=False)

class Coref(Base):
    __tablename__ = "coreference"
    coref_id = Column("coref_id", Integer, primary_key=True)
    question_id = Column("question_id", Integer, ForeignKey("question.question_id"), nullable=False)
    mention_pair_id = Column("mention_pair_id", Integer, ForeignKey("mention_pair.mention_pair_id"), nullable=False)
    description = Column("description", Text)
    same = Column("same", Boolean, nullable=False)
    author = Column("author", ForeignKey("user.user_id"), nullable=False)
    date_added = Column("date_added", DateTime, default=datetime.datetime.utcnow(), nullable=False)
    UniqueConstraint('mention_pair_id', 'author', name='no_dups')

class User(Base):
    __tablename__ = "user"
    user_id = Column("user_id", Integer, primary_key=True)
    username = Column("username", String(255), nullable=False)
    password = Column("password", String(255), nullable=False)
    first_name = Column("first_name", String(255), nullable=False)
    last_name = Column("last_name", String(255), nullable=False)
    email = Column("email", String(255), nullable=False)
    last_qid = Column("last_qid", Integer, ForeignKey('question.question_id'))
    last_login = Column("last_login", DateTime)
    is_admin = Column("is_admin", Boolean, nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'last_login': str(self.last_login),
        }

class UserQuestion(Base):
    __tablename__ = "user_question"
    user_question_id = Column("user_question_id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False)
    question_id = Column("question_id", Integer, ForeignKey("question.question_id"), nullable=False)
    finished = Column("finished", Boolean, default=False, nullable=False)

class Mention(Base):
    __tablename__ = "mention"
    mention_id = Column("mention_id", Integer, primary_key=True)
    question_id = Column("question_id", Integer, ForeignKey("question.question_id"), nullable=False)
    pos_start = Column("pos_start", Integer, nullable=False)
    pos_end = Column("pos_end", Integer, nullable=False)

    def to_dict(self):
        return {
            'mention_id': self.mention_id,
            'question_id': self.question_id,
            'pos_start': self.pos_start,
            'pos_end': self.pos_end,
        }

class MentionPair(Base):
    __tablename__ = "mention_pair"
    mention_pair_id = Column("mention_pair_id", Integer, primary_key=True)
    mention_id_1 = Column("mention_id_1", Integer, ForeignKey("mention.mention_id"), nullable=False)
    mention_id_2 = Column("mention_id_2", Integer, ForeignKey("mention.mention_id"), nullable=False)
    mention1 = relationship(Mention, foreign_keys=mention_id_1)
    mention2 = relationship(Mention, foreign_keys=mention_id_2)
    question_id = Column("question_id", Integer, ForeignKey("question.question_id"), nullable=False)
    user_mention_pairs = relationship("Coref", backref="mention_pair")
    score = Column("score", Float)

    def to_dict(self):
        return {
            'mention_pair_id': self.mention_pair_id,
            'mention1': self.mention1.to_dict(),
            'mention2': self.mention2.to_dict(),
            'question_id': self.question_id,
            'score': self.score,
        }

    def __repr__(self):
        return "MentionPair(pair1=%u, pair2=%u, score=%f)" % (
            self.mention_id_1,
            self.mention_id_2,
            self.score
        )

    def __str__(self):
        return repr(self)

class UserMentionPair(Base):
    __tablename__ = "user_mention_pair"
    user_mention_pair_id = Column("user_mention_pair_id", Integer, primary_key=True)
    mention_pair_id = Column("mention_pair_id", Integer, ForeignKey("mention_pair.mention_pair_id"))
    annotation = Column("annotation", Boolean, nullable=False)

    def __repr__(self):
        return "UserMentionPair(%s)" % self.mention_pair_id

    def __str__(self):
        return repr(self)

Base.metadata.create_all(engine)

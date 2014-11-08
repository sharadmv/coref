import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey

Base = declarative_base()

engine = create_engine("mysql://coref@localhost/coref")

class Question(Base):
    __tablename__ = "questions"
    question_id = Column("question_id", Integer, primary_key=True)
    question = Column("question", Text, nullable=False)

class Answer(Base):
    __tablename__ = "answers"
    answer_id = Column("answer_id", Integer, primary_key=True)
    question_id = Column("question_id", Integer, ForeignKey("questions.question_id"), nullable=False)
    answer = Column("answer", Text, nullable=False)

class Coref(Base):
    __tablename__ = "coreferences"
    coref_id = Column("coref_id", Integer, primary_key=True)
    question_id = Column("question_id", Integer, ForeignKey("questions.question_id"), nullable=False)
    mention_id_1 = Column("mention_id_1", Integer, ForeignKey("mentions.mention_id"), nullable=False)
    mention_id_2 = Column("mention_id_2", Integer, ForeignKey("mentions.mention_id"), nullable=False)
    description = Column("description", Text, nullable=False)
    same = Column("same", Boolean, nullable=False)
    author = Column("author", ForeignKey("users.user_id"), nullable=False)
    date_added = Column("date_added", DateTime, default=datetime.datetime.utcnow(), nullable=False)

class User(Base):
    __tablename__ = "users"
    user_id = Column("user_id", Integer, primary_key=True)
    username = Column("username", String(255), nullable=False)
    password = Column("password", String(255), nullable=False)
    first_name = Column("first_name", String(255), nullable=False)
    last_name = Column("last_name", String(255), nullable=False)
    email = Column("email", String(255), nullable=False)
    last_qid = Column("last_qid", Integer, ForeignKey('questions.question_id'))
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
            'email': self.email
        }

class Mention(Base):
    __tablename__ = "mentions"
    mention_id = Column("mention_id", Integer, primary_key=True)
    question_id = Column("question_id", Integer, ForeignKey("questions.question_id"), nullable=False)
    pos_start = Column("pos_start", Integer, nullable=False)
    pos_end = Column("pos_end", Integer, nullable=False)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

#if __name__ == "__main__":
    #from sqlalchemy.orm import sessionmaker
    #Session = sessionmaker()
    #Session.configure(bind=engine)
    #user = User(uid=1,
                #username='sharad',
                #password='sharad',
                #first_name='sharad',
                #last_name='sharad',
                #email='sharad',
                #last_qid=0,
                #is_admin=True,
                #last_login=datetime.datetime.now()
                #)
    #session = Session()
    #session.add(user)
    #session.commit()

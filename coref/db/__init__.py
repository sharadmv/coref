from sqlalchemy.orm import sessionmaker

from model import Question, Answer, Coref, User, Mention, MentionPair, engine, UserQuestion, UserMentionPair

Session = sessionmaker()
Session.configure(bind=engine)

class WithSession:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self.session

    def __exit__(self, type, value, traceback):
        self.session.close()


def session():
    return WithSession(Session())

with session() as s:
    QUESTION_IDS = [q.question_id for q in s.query(Question)]

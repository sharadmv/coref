from sqlalchemy.orm import sessionmaker

from model import Question, Answer, Coref, User, Mention, engine

Session = sessionmaker()
Session.configure(bind=engine)

def session():
    return Session()

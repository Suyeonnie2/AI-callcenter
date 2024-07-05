from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question_text = Column(String)

engine = create_engine('sqlite:///questions.db')
Session = sessionmaker(bind=engine)
session = Session()

def query(intent):
    question = session.query(Question).filter_by(intent=intent).first()
    return question

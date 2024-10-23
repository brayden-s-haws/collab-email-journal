import os
from datetime import date, datetime, timedelta

from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from question_gen import new_question

## SETUP DATABASE CONNECTION ##
db_url = os.environ.get('DATABASE_URL')


def create_session(db_url):
    """
    Create a database session.
    """
    engine = create_engine(db_url, connect_args={'options': '-csearch_path=couples_journal'})
    Session = sessionmaker(bind=engine)
    return Session()


def setup_base_class():
    """
    Setup the declarative base class.
    """
    return declarative_base()


class Question(setup_base_class()):
    __tablename__ = 'questions'
    __table_args__ = {'schema': 'couples_journal'}

    question_id = Column(Integer, primary_key=True)
    question_text = Column(String)
    question_date = Column(Date, default=date.today)
    created_at = Column(DateTime, default=datetime.now)

def write_new_question(session, new_question):
    """
    Writes newly generated question to the database.
    """
    new_question_details = Question(question_text=new_question)
    session.add(new_question_details)
    session.commit()
    session.close()


## WRITE NEW QUESTION TO DATABASE ##

# Create a session
session = create_session(db_url)

write_new_question(session, new_question)


## WRITE RESONSES TO DATABASE ##
# TODO: Setup write of responses to the database
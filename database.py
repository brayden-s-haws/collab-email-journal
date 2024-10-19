import os
from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
    __tablename__ = 'responses'

    response_id = Column(Integer, primary_key=True)
    user_email = Column(String)
    question_id = Column(Integer)
    response_text = Column(String)
    response_date = Column(Date)
    created_at = Column(Date)
    schema = 'couples_journal'


def get_previous_questions(session, start_date):
    """
    Retrieve questions from the database from a given start date.
    """
    questions = session.query(Question).filter(Question.question_date > start_date).all()
    session.close()
    return questions
  

def format_questions(questions):
    """
    Format questions into a single string.
    """
    return '; '.join([question.question_text for question in questions])


# Create a session
session = create_session(db_url)

# Get the current date
one_year_ago = datetime.now().date() - timedelta(days=365)

# Fetch and format previous questions
previous_questions_fetch = get_previous_questions(session, one_year_ago)
previous_questions = format_questions(previous_questions_fetch)


## WRITE NEW QUESTION TO DATABASE ##

class Response(setup_base_class()):
  __tablename__ = 'responses'

  response_id = Column(Integer, primary_key=True)
  question_text = Column(String)
  question_date = Column(Date)
  created_at = Column(Date)
  schema = 'couples_journal'


# TODO: Setup write of new question from the LLM response
  #TODO: function for writing back
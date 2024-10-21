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
    __tablename__ = 'questions'

    question_id = Column(Integer, primary_key=True)
    question_text = Column(String)
    question_date = Column(Date)
    created_at = Column(Date)
    schema = 'couples_journal'


## WRITE NEW QUESTION TO DATABASE ##

# TODO: Setup write of new question from the LLM response
  #TODO: Class for response
  #TODO: function for writing back



## WRITE RESONSES TO DATABASE ##
# TODO: Setup write of responses to the database
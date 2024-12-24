import os
from datetime import date, datetime, timedelta

from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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

# Define the question class for the database
class Question(setup_base_class()):
    __tablename__ = 'questions'
    __table_args__ = {'schema': 'couples_journal'}

    question_id = Column(Integer, primary_key=True)
    question_text = Column(String)
    question_date = Column(Date, default=date.today)
    created_at = Column(DateTime, default=datetime.now)

# Write the new question to the database
def write_new_question(new_question):
    """
    Writes newly generated question to the database.
    """
    db_url = os.environ.get('DATABASE_URL')
    session = create_session(db_url)
    new_question_details = Question(question_text=new_question)
    session.add(new_question_details)
    session.commit()
    session.close()

## WRITE RESONSES TO DATABASE ##
    # TODO: Define a class for the reponse
    # TODO: Setup write of responses to the database
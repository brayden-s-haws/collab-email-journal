import os

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

## SETUP DATABASE CONNECTION ##
db_url = os.environ.get('DATABASE_URL')

# Create the SQLAlchemy engine
engine = create_engine(db_url, connect_args={'options': '-csearch_path=couples_journal'})

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Setup questions base class
Base = declarative_base()

class Question(Base):
  __tablename__ = 'questions'

  question_id = Column(Integer, primary_key=True)
  question_text = Column(String)
  question_date = Column(Date)
  created_at = Column(Date)
  schema = 'couples_journal'

previous_questions_fetch = session.query(Question).all()
"""
for question in previous_questions_fetch:
    print(f"ID: {question.question_id}, Question: {question.question_text}, Date: {question.question_date}")
"""

previous_questions = '; '.join([question.question_text for question in previous_questions_fetch])

# print(previous_questions)


# TODO: Setup write of new question from the LLM response
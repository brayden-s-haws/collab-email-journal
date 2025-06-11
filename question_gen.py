import os
from datetime import datetime, timedelta

from anthropic import Anthropic
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def create_session():
    """
    Create a database session.
    """
    db_url = os.environ.get('DATABASE_URL')
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
    question_date = Column(Date)
    created_at = Column(DateTime)


def get_previous_questions():
    """
    Retrieve questions from the database from a given start date.
    """
    session = create_session()
    start_date = datetime.now().date() - timedelta(days=365)
       
    questions = session.query(Question).filter(Question.question_date > start_date).all()
    question_temp_id = max(question.question_id for question in questions) + 1
    session.close()
    return questions, question_temp_id


def format_questions():
    """
    Format the retrieved questions into a single string.
    """
    questions, question_temp_id = get_previous_questions()
    return '; '.join(question.question_text for question in questions), question_temp_id


def create_formatted_prompt(question_gen_prompt):
    """
    Create a formatted prompt for the Anthropic API. Inserts the retrieved questions into the prompt.
    """
    previous_questions, question_temp_id = format_questions()
    # This is the prompt that will be used to generate the new question includes a placeholder for the previous questions
    question_gen_prompt = question_gen_prompt
    
    formatted_prompt = question_gen_prompt.format(previous_questions=previous_questions)
    return formatted_prompt, question_temp_id
    

# Get a new question from Claude and generate a temp id for use in matching responses
def get_claude_question(question_gen_prompt):
    """
    Give Claude the formatted prompt and get a question back.
    """
    formatted_prompt, question_temp_id = create_formatted_prompt(question_gen_prompt)
    claude_client = Anthropic()
    message = claude_client.messages.create(model = "claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.7,
            messages=[{"role": "user", "content": formatted_prompt,}],
  )
    return message.content[0].text, question_temp_id



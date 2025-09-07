import os
import schedule
import time
from datetime import datetime
import pytz
import threading

from email_build import send_email
from question_gen import get_claude_question
from database_write import write_new_question
from email_build import send_email
from config import start_email_webhook_server,question_gen_prompt

# Environment variables
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
SENDGRID_LIST = os.environ['SENDGRID_LIST']
SENDGRID_EMAIL_FROM = os.environ['SENDGRID_EMAIL_FROM']
SENDGRID_EMAIL_CC = os.environ['SENDGRID_EMAIL_CC']
SENDGRID_EMAIL_RESPONSE = os.environ['SENDGRID_EMAIL_RESPONSE']

# Configure the email flow
def email_flow():
  # Get the new question from Claude and generate a temp id for use in matching responses
  new_question, question_temp_id = get_claude_question(question_gen_prompt)
  print(new_question)
  print(question_temp_id)
  
  # Write the new question to the database
  write_new_question(new_question)
  
  # Send the new question to the email list
  send_email(SENDGRID_API_KEY, SENDGRID_LIST, SENDGRID_EMAIL_FROM, SENDGRID_EMAIL_CC, SENDGRID_EMAIL_RESPONSE, new_question, question_temp_id)

# Schedule the email to be sent on a schedule
def email_schedule():
  schedule.every().wednesday.at("02:05").do(email_flow)
  print("Email flow scheduled to run.")
  while True:
    schedule.run_pending()
    print("Email flow running.")
    time.sleep(30)

# Start the scheduler and webhook server in separate threads
email_schedule_thread = threading.Thread(target=email_schedule)
webhook_thread = threading.Thread(target=start_email_webhook_server)
email_schedule_thread.start()
webhook_thread.start()


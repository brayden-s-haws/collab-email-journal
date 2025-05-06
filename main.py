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
from response_fetch import start_email_webhook_server

# Environment variables
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
SENDGRID_LIST = os.environ['SENDGRID_LIST']
SENDGRID_EMAIL_FROM = os.environ['SENDGRID_EMAIL_FROM']
SENDGRID_EMAIL_CC = os.environ['SENDGRID_EMAIL_CC']
SENDGRID_EMAIL_RESPONSE = os.environ['SENDGRID_EMAIL_RESPONSE']

# Configure the email flow
def email_flow():
  # Get the new question from Claude and generate a temp id for use in matching responses
  new_question, question_temp_id = get_claude_question()
  print(new_question)
  print(question_temp_id)
  
  # Write the new question to the database
  write_new_question(new_question)
  
  # Send the new question to the email list
  send_email(SENDGRID_API_KEY, SENDGRID_LIST, SENDGRID_EMAIL_FROM, SENDGRID_EMAIL_CC, SENDGRID_EMAIL_RESPONSE, new_question, question_temp_id)

# Schedule the email to be sent on a schedule


def email_send_scheduler():
  email_sent_this_week = False
  last_day_checked = -1

  while True:
    mountain_timezone = pytz.timezone('US/Mountain')
    now = datetime.now(mountain_timezone)
    print(f"Current time in Mountain Time: {now}")

    if now.weekday() == 0 and last_day_checked != 0:
      print("Resetting email_sent_this_week flag.")
      email_sent_this_week = False
  
    if now.weekday() == 6 and now.hour == 19 and now.minute >= 47 and now.minute < 48:
          print("Running email flow...")
          email_flow()
          email_sent_this_week = True
  
    time.sleep(5)

# Start the scheduler and webhook server in separate threads
email_schedule_thread = threading.Thread(target=email_send_scheduler)
webhook_thread = threading.Thread(target=start_email_webhook_server)
email_schedule_thread.start()
webhook_thread.start()


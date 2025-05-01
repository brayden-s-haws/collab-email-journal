import os
import schedule
import time
import pytz
import threading

from email_build import send_email
from question_gen import get_claude_question
from database_write import write_new_question
from email_build import send_email
from response_fetch import start_webhook_server

# Environment variables
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
sendgrid_list = os.environ['SENDGRID_LIST']
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
  send_email(SENDGRID_API_KEY, sendgrid_list, SENDGRID_EMAIL_FROM, SENDGRID_EMAIL_RESPONSE, SENDGRID_EMAIL_CC, new_question, question_temp_id)

# Schedule the email to be sent on a schedule
mountain_timezone = pytz.timezone('US/Mountain')
schedule.every().sunday.at("19:38").do(email_flow)

def run_scheduler():
    while True:
        print("Checking for scheduled tasks...")
        schedule.run_pending()
        time.sleep(60)

# Start the scheduler and webhook server in separate threads
scheduler_thread = threading.Thread(target=run_scheduler)
webhook_thread = threading.Thread(target=start_webhook_server)
scheduler_thread.start()
webhook_thread.start()


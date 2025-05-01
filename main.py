import os
import schedule
import time
import pytz

from email_build import send_email
from question_gen import get_claude_question
from database_write import write_new_question
from email_build import send_email
from response_fetch import start_webhook_server

SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
sendgrid_list = os.environ['SENDGRID_LIST']
SENDGRID_EMAIL_FROM = os.environ['SENDGRID_EMAIL_FROM']
SENDGRID_EMAIL_CC = os.environ['SENDGRID_EMAIL_CC']
SENDGRID_EMAIL_RESPONSE = os.environ['SENDGRID_EMAIL_RESPONSE']

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
schedule.every().sunday.at("09:00").do(email_flow)


# (Wrap ⬆️ these in a cron)
# Grab email responses and write them to the database
start_webhook_server()





# TODOs:
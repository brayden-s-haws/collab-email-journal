import os
import re
from flask import Flask, request, render_template
from database_write import write_new_response
from email_build import get_contact_emails_from_list_name
from config import app

def extract_response_from_email(subject, email_content):
    """
    Extract the response and question ID from the email.
    """
    # Extract the question ID from the subject
    question_id_search = re.search(r'\((\d+)\)', subject)
    question_id = int(question_id_search.group(1)) if question_id_search else None

    # Extract the response from the email text
    text_match =  re.search(r'Content-Type: text/plain;.*?Content-Transfer-Encoding:[^\r\n]*\r\n\r\n(.*?)(?:\r\n\r\n----==|$)', email_content, re.DOTALL)

    response_text =  text_match.group(1).split('On ')[0] if text_match else None

    print(response_text)

    return question_id, response_text


@app.route('/email/webhook', methods=['GET', 'POST'])
def response_webhook():
  """
  Fetch the email responses from the webhook.
  """
  # Check if the request is a GET request
  if request.method == 'GET':
      return "Webhook is running", 200
      
  # Check if the request is a POST request
  elif request.method == 'POST':
      # Extract the email data from the request
      raw_user_email = request.form.get('from')
      user_email = raw_user_email.split('<')[1].split('>')[0]
      subject = request.form.get('subject')
      email_content = request.form.get('email')

      def check_emails():
          # Check if the email is in the allowed list
          from main import SENDGRID_API_KEY, SENDGRID_LIST
          allowed_emails = get_contact_emails_from_list_name(SENDGRID_API_KEY, SENDGRID_LIST)
          return allowed_emails
          
      allowed_emails = check_emails()
      
      if user_email in allowed_emails:
          # Extract the response and question ID from the email
          question_id, response_text = extract_response_from_email(subject, email_content)
        
          # Write the response to the database
          write_new_response(user_email, question_id, response_text)
        
          # Return a response to acknowledge receipt of the email
          return "OK", 200
      else:
          print("Unauthorized email address:", user_email)
          return "Email not in allowed list", 200 # Return 200 to avoid retrying the webhook, should be 403 but Sendgrid doesn't seem to support it and keeps retrying for up to 72 hours
          

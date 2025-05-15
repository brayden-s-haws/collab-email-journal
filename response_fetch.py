import os
import re
from flask import Flask, request
from database_write import write_new_response

app = Flask(__name__)

# TODO: Move this to a config file
@app.route('/', methods=['GET'])
def index():
    """
    Simple handler for the root path to avoid 404 errors.
    """
    return "Couples Journal API is running", 200

def extract_response_from_email(subject, text):
    """
    Extract the response and question ID from the email.
    """
    # Extract the question ID from the subject
    question_id_search = re.search(r'\((\d+)\)', subject)
    question_id = int(question_id_search.group(1)) if question_id_search else None

    # Extract the response from the email text
    response_text =  text.strip()if text else None

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
      user_email = request.form.get('from')
      subject = request.form.get('subject')
      text = request.form.get('text')
      body = request.form.get('hmtl')
      print(user_email)
      print(subject)
      print(text)
      print(body)
      
      # Extract the response and question ID from the email
      question_id, response_text = extract_response_from_email(subject, text)
    
      # Write the response to the database
      write_new_response(user_email, question_id, response_text)
    
      # Return a response to acknowledge receipt of the email
      return "OK", 200

def start_email_webhook_server():
    """
    Start the webhook server.
    """
    app.run(host ='0.0.0.0', debug=True, port=5000, use_reloader= False, threaded=True)

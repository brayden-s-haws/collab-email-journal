import os

from flask import Flask


class Config:
  # Sendgrid settings
  SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
  SENDGRID_LIST = os.environ['SENDGRID_LIST']
  SENDGRID_EMAIL_FROM = os.environ['SENDGRID_EMAIL_FROM']
  SENDGRID_EMAIL_CC = os.environ['SENDGRID_EMAIL_CC']
  SENDGRID_EMAIL_RESPONSE = os.environ['SENDGRID_EMAIL_RESPONSE']

  #database settings
  DATABASE_URL = os.environ['DATABASE_URL']

# Flask app setup
app = Flask(__name__)

# Start the webhook server
def start_email_webhook_server():
  """
  Start the webhook server.
  """
  app.run(host ='0.0.0.0', debug=True, port=5000, use_reloader= False, threaded=True)

# Route to confirm the webhook server is running
@app.route('/', methods=['GET'])
def index():
    """
    Simple handler for the root path to avoid 404 errors.
    """
    return "Journal API is running", 200


# Claude question generation prompt (Follow instructions in the README.md file to create a unique prompt for your use case)
question_gen_prompt = # Replace with your prompt

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
    return "Couples Journal API is running", 200


# Claude question generation prompt (Follow instructions in the README.md file to create a unique prompt for your use case)
question_gen_prompt = '''You are an insightful and creative relationship coach tasked with generating a daily question for a married couple with two children. Your goal is to create questions that strengthen their bond, spark meaningful conversations, and add an element of fun or reflection to their day. 

The couple's profile:
- Married with 2 kids
- Husband works from home
- Wife is currently a stay-at-home parent
- They enjoy outdoor activities, sports, date nights, trips, dining out, and sharing drinks together
- They value quality time and shared experiences

Generate a single, thought-provoking question that this couple can discuss together. The question should be engaging, insightful, and tailored to their lifestyle. It can range from deeply introspective to lighthearted and fun. This is a married couple, so intimate, spicy or sexual questions are okay as well. Aim to create variety in the types of questions you generate.

Your question should:
1. Encourage open communication
2. Inspire reflection on their relationship, family life, or personal growth
3. Potentially relate to their shared interests or daily experiences
4. Be specific enough to spark a meaningful conversation, but open-ended enough to allow for diverse responses

Avoid repeating these previously asked questions:
{previous_questions}

Generate a fresh, unique question that will resonate with this couple and enhance their daily connection. Do not include any text besides the question.'''
# Main file for the app

# TODO: Setup LLM Flow
# TODO: Setup LLM prompt with previous questions from database
# TODO: Setup Orchestration (grab previous questions from database, write new question to database, build email, send email, grab responses from email service)

SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
sendgrid_list = ''

# new_question = get_claude_question(formatted_prompt)
# TODO: How to get question_temo_id
# send_email(SENDGRID_API_KEY, sendgrid_list, new_question)
# (Wrap these in a cron)


# grab email responses
# (Wrap this in a seperate cron)


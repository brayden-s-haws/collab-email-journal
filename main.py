from question_gen import get_claude_question
from database_write import write_new_question


new_question, question_temp_id = get_claude_question()
print(new_question)
print(question_temp_id)

write_new_question(new_question)





# TODO: Setup email builder (HTML, get emails from fetch_emails)
#SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
#sendgrid_list = os.environ['SENDGRID_LIST']
# send_email(SENDGRID_API_KEY, sendgrid_list, new_question)
# (Wrap these in a cron)


# grab email responses
# (Wrap this in a seperate cron)


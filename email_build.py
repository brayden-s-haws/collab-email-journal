# TODO: Setup email builder (HTML, get emails from fetch_emails)
import json
import os 

from sendgrid import SendGridAPIClient

from sendgrid.helpers.mail import Mail

def get_contact_emails_from_list_name(api_key, list_name):
    """
    :param str api_key: Your Sendgrid API KEY
    :param str list_name: The contact list you wish to send the email to
    :return: list
    """
    sg = SendGridAPIClient(api_key=api_key)

    try:
        # Fetch all lists
        response = sg.client.marketing.lists.get(query_params={'page_size': 1000})
        lists_data = json.loads(response.body)

        # Find the list_id for the specified list_name
        list_id = None
        for lst in lists_data['result']:
            if lst['name'] == list_name:
                list_id = lst['id']
                break

        if not list_id:
            print(f"No list found with the name: {list_name}")
            return []

        # Fetch contacts from the specified list
        response = sg.client.marketing.contacts.search.post(request_body={
            "query": f"CONTAINS(list_ids, '{list_id}')"
        })

        contacts_data = json.loads(response.body)
        emails = [contact['email'] for contact in contacts_data['result']]

        # TODO: Handle potential pagination if you expect more than 1000 contacts.
        print(f"Retrieved {len(emails)} emails.")

        return emails

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def send_email(SENDGRID_API_KEY, sendgrid_list, SENDGRID_EMAIL, new_question, question_temp_id):
    recipients = get_contact_emails_from_list_name(SENDGRID_API_KEY, sendgrid_list)
    message = Mail(
      from_email=SENDGRID_EMAIL,  # This needs to match an email that you have verified with SendGrid
      to_emails=SENDGRID_EMAIL,  # Put your email here so that you receive it when sent to the BCC'd recipients .
      subject=f"Today's Couples Question ({question_temp_id})",  # The subject for the email
      html_content=new_question
    )
    # Add each email as BCC
    for email in recipients:
      message.add_bcc(email)

    try:
      sg = SendGridAPIClient(SENDGRID_API_KEY)
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
    except Exception as e:
      print("Error sending the email:", e)
      if hasattr(e, 'body'):
          print(e.body)


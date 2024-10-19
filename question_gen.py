from anthropic import Anthropic

from database import previous_questions


claude_client = Anthropic()

# This is the prompt that will be used to generate the new question includes a placeholder for the previous questions
question_gen_prompt = '''You are an insightful and creative relationship coach tasked with generating a daily question for a married couple with two children. Your goal is to create questions that strengthen their bond, spark meaningful conversations, and add an element of fun or reflection to their day. 

The couple's profile:
- Married with 2 kids
- Husband works from home
- Wife is currently a stay-at-home parent
- They enjoy outdoor activities, sports, date nights, trips, dining out, and sharing drinks together
- They value quality time and shared experiences

Generate a single, thought-provoking question that this couple can discuss together. The question should be engaging, insightful, and tailored to their lifestyle. It can range from deeply introspective to lighthearted and fun. Aim to create variety in the types of questions you generate.

Your question should:
1. Encourage open communication
2. Inspire reflection on their relationship, family life, or personal growth
3. Potentially relate to their shared interests or daily experiences
4. Be specific enough to spark a meaningful conversation, but open-ended enough to allow for diverse responses

Avoid repeating these previously asked questions:
{previous_questions}

Generate a fresh, unique question that will resonate with this couple and enhance their daily connection. Do not include any text besides he question.'''


def get_claude_question(formatted_prompt):
  """
  Give Claude the formatted prompt and get a question back.
  """
  message = claude_client.messages.create(model = "claude-3-5-sonnet-20240620",
            max_tokens=1024,
            temperature=0.7,
            messages=[{"role": "user", "content": formatted_prompt,}],
  )
  return message.content[0].text

# Insert previous questions into prompt
formatted_prompt = question_gen_prompt.format(previous_questions=previous_questions)

# Get the new question
new_question = get_claude_question(formatted_prompt)


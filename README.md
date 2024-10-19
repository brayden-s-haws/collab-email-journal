# Notes for setup:


## Question Creation Prompt

You'll need to replace the prompt with a prompt unique to your use case. Fill out this template and put it into the LLM of your choice to generate the prompt. Be sure to include instructions to include {previous_questions} in the prompt

Create a comprehensive prompt for an AI language model to generate daily questions for a specific audience. The prompt should include the following elements:

1. Context: Provide a brief description of the AI's role and the purpose of the questions it will generate.

2. Audience profile: Include key details about the target audience, such as:
   - Demographic information
   - Relationship status
   - Family structure
   - Occupation
   - Interests and hobbies
   - Values and priorities

3. Question guidelines: Specify the characteristics of the questions to be generated, including:
   - Tone (e.g., introspective, lighthearted, challenging)
   - Purpose (e.g., spark conversation, encourage reflection, strengthen bonds)
   - Structure (e.g., open-ended, specific but not restrictive)

4. Diversity instructions: Include directions for ensuring variety in the types of questions generated.

5. Relevance criteria: Explain how the questions should relate to the audience's lifestyle and interests.

6. Constraints: Mention any topics or types of questions to avoid.

7. Uniqueness requirement: Include instructions for avoiding repetition, possibly by referencing previously asked questions.

8. Output format: Specify how the AI should present its generated question.

Ensure the prompt is clear, concise, and provides enough detail for the AI to generate high-quality, tailored questions consistently. The resulting prompt should be adaptable to different audiences by modifying the audience profile and specific guidelines.



## Setup Database Schema
You'll need a postgres database with the following tables. Store the database details as environment variables

CREATE SCHEMA IF NOT EXISTS schema_name;

## Add Tables
CREATE TABLE schema_name.users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP
);


CREATE TABLE schema_name.questions (
    question_id SERIAL PRIMARY KEY,
    question_text VARCHAR NOT NULL,
    question_date DATE NOT NULL,
    created_at TIMESTAMP
);


CREATE TABLE schema_name.responses (
    response_id SERIAL PRIMARY KEY,
    user_email VARCHAR(100) NOT NULL,
    question_id BIGINT  NOT null,
    response_text VARCHAR NOT NULL,
    response_date DATE NOT NULL,
    created_at TIMESTAMP
);

INSERT INTO  schema_name.users
(first_name, last_name, email, created_at)
VALUES 
('','','',CURRENT_TIMESTAMP);


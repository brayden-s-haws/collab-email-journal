# Couples Journal - Daily Question Email System

#### Current status: Complete

___

### Personal Progress
* **What I learned**: Multi-service integration patterns, webhook handling, email automation with SendGrid, AI prompt engineering for consistent question generation, and database design for relationship tracking
* **What I wish I had done differently**: Started with a more structured approach using classes and type hints. Also would have implemented true logging and error handling
* **What I am most proud of**: Successfully orchestrating multiple APIs (Anthropic, SendGrid, PostgreSQL) into a cohesive system that creates meaningful daily touchpoints for my relationship
* **What I want to learn next**: Refactoring this codebase to use proper Python patterns including classes, type hints, comprehensive logging, and test coverage. Also interested in adding a web interface for browsing past questions and responses

## Description
Maintaining meaningful daily communication in busy relationships can be challenging. This Couples Journal system solves this by automatically generating and sending thoughtful daily questions via email, then capturing and storing responses to build a shared relationship journal over time.

The system uses AI to generate personalized questions based on the couple's interests and lifestyle, sends them via email at scheduled times, and processes responses through an automated webhook system. All questions and responses are stored in a database, creating a growing archive of the relationship's journey.

## How It Works
This diagram provides a high-level view of how the system works:
<img width="2544" height="1764" alt="CleanShot Freeform-2025-09-09" src="https://github.com/user-attachments/assets/5f268aab-e5e9-4297-90e7-70958c1d34c7" />

The system orchestrates multiple services to create a seamless daily question experience:

```mermaid
graph TD
    A[Scheduled Trigger] --> B[Retrieve Previous Questions]
    B --> C[Generate New Question with Claude]
    C --> D[Store Question in Database]
    D --> E[Send Email via SendGrid]
    E --> F[Email Delivered to Couple]
    F --> G[Couple Responds via Email]
    G --> H[SendGrid Webhook Triggered]
    H --> I[Extract Response Content]
    I --> J[Store Response in Database]
    J --> K[Archive for Future Reference]
```
This is an example question that was generated from a prompt focused on a married couple:
<img width="1422" height="196" alt="CleanShot HEY-2025-09-09" src="https://github.com/user-attachments/assets/4c859d44-2450-4337-a3ee-f86266532baa" />

Here's how the question generation process ensures variety and relevance:

```mermaid
graph TD
    A[Question Generation Request] --> B[Query Database for Past Year Questions]
    B --> C[Format Previous Questions as Context]
    C --> D[Send to Claude with Custom Prompt]
    D --> E[Generate Unique Question]
    E --> F[Validate Against Duplicates]
    F --> G{Question is Unique?}
    G -->|Yes| H[Return New Question]
    G -->|No| I[Regenerate Question]
    I --> D
```

## Features
This describes the key capabilities that make the couples journal system effective:

- **AI-Powered Question Generation**: Uses Anthropic's Claude to create personalized, varied questions based on the couple's profile and interests
- **Duplicate Prevention**: Tracks all previous questions for the past year to ensure fresh, unique content
- **Automated Email Delivery**: Scheduled email sending via SendGrid to a curated contact list
- **Response Collection**: Webhook system automatically captures and stores email replies
- **Database Archiving**: PostgreSQL storage for all questions and responses, creating a permanent relationship journal
- **Flexible Scheduling**: Configurable timing for question delivery (currently set for Wednesday mornings)
- **Security Controls**: Email validation ensures only authorized contacts can submit responses

## Customization Guide
This system is designed to be easily adapted for different couples or relationship types:

1. **Personalize Question Prompts**: 
   
   You'll need to replace the current prompt with a prompt unique to your use case. **Follow these steps to create your custom prompt:**
   /n
   **Step 1**: Use this template in any LLM (ChatGPT, Claude, etc.) to generate your personalized prompt:
   
   ```
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

   **CRITICAL**: The generated prompt MUST include the exact text "{previous_questions}" somewhere in the uniqueness/repetition avoidance section. This placeholder is essential for the system to work properly.
   ```
   
   **Step 2**: Review the generated prompt and **verify it contains `{previous_questions}`** as a placeholder in the section about avoiding repetition.
   
   **Step 3**: Copy the complete generated prompt and paste it as the value for `question_gen_prompt` in the `config.py` file, replacing the existing prompt.
   
   **Example of what to look for**: Your generated prompt should include something like:
   ```
   "Avoid repeating these previously asked questions: {previous_questions}"
   ```

2. **Configure Email Settings**: 
   - Set up SendGrid API key and verified sender domains
   - Create contact lists for email recipients
   - Customize email templates and subject lines

3. **Database Schema**: 
   - Add custom fields to track relationship-specific data
   - Extend response categories or add tagging systems
   - Create additional tables for analytics or insights

4. **Scheduling Options**: 
   - Modify timing in main.py for different delivery schedules
   - Add multiple question types for different days
   - Implement seasonal or event-based question themes

## Files
This describes the role of key files in creating the couples journal experience:

- **main.py**: Application entry point that manages scheduling and coordinates all system components
- **question_gen.py**: Handles AI question generation, database queries for previous questions, and prompt formatting
- **email_build.py**: Manages SendGrid integration for both retrieving contact lists and sending formatted emails
- **response_fetch.py**: Flask webhook server that processes incoming email responses and validates senders
- **database_write.py**: Database operations for storing questions and responses using SQLAlchemy
- **config.py**: Configuration management for environment variables and application settings
- **routes.py**: Flask route definitions (currently empty, ready for web interface expansion)

## Setup
The system requires minimal compute resources since it primarily orchestrates API calls and database operations. Here's how to set it up:

1. **Clone and Install Dependencies**:
   ```bash
   git clone [your-repo-url]
   cd couples-journal
   poetry install
   ```

2. **Database Setup**:
   ```sql
   CREATE SCHEMA couples_journal;
   
   CREATE TABLE couples_journal.users (
       user_id SERIAL PRIMARY KEY,
       first_name VARCHAR(50) NOT NULL,
       last_name VARCHAR(50) NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       created_at TIMESTAMP
   );
   
   CREATE TABLE couples_journal.questions (
       question_id SERIAL PRIMARY KEY,
       question_text VARCHAR NOT NULL,
       question_date DATE NOT NULL,
       created_at TIMESTAMP
   );
   
   CREATE TABLE couples_journal.responses (
       response_id SERIAL PRIMARY KEY,
       user_email VARCHAR(100) NOT NULL,
       question_id BIGINT NOT NULL,
       response_text VARCHAR NOT NULL,
       response_date DATE NOT NULL,
       created_at TIMESTAMP
   );
   ```

3. **Environment Variables**:
   ```bash
   export SENDGRID_API_KEY=your_sendgrid_api_key
   export SENDGRID_LIST=your_contact_list_name
   export SENDGRID_EMAIL_FROM=verified_sender@yourdomain.com
   export SENDGRID_EMAIL_CC=your_email@domain.com
   export SENDGRID_EMAIL_RESPONSE=responses@yourdomain.com
   export DATABASE_URL=postgresql://user:password@localhost:5432/database
   export ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

4. **SendGrid Webhook Configuration**:
   - Set up inbound email parsing in SendGrid
   - Configure webhook URL to point to `/email/webhook` endpoint
   - Verify sender domains and email authentication

5. **Run the Application**:
   ```bash
   python main.py
   ```

## Technical Architecture

**Key Packages/Tools**:
- **Anthropic**: AI question generation with Claude models
- **SendGrid**: Email delivery and inbound webhook processing  
- **SQLAlchemy**: Database ORM for PostgreSQL operations
- **Flask**: Lightweight web server for webhook handling
- **Schedule**: Python job scheduling for automated email sending
- **Poetry**: Dependency management and virtual environment

**Planned Improvements** (Next Phase):
- Refactor to use Python classes for better organization
- Add comprehensive type hints throughout codebase
- Implement structured logging for debugging and monitoring
- Create comprehensive test suite with unit and integration tests
- Build web interface for browsing question/response history
- Add analytics dashboard for relationship insights

## License

This project is open source and available under the [MIT License](LICENSE).

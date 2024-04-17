import streamlit as st
import re
from langchain_anthropic import ChatAnthropic
from langchain import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
import mcq_component

# Load the .env file to get the API keys
load_dotenv()
apikey = os.environ["ANTHROPIC_API_KEY"]

# Initialize the chat model with Anthropic API key
llm = ChatAnthropic(anthropic_api_key=apikey, model_name="claude-3-opus-20240229")

# Define a prompt template for generating MCQs
mcq_prompt = PromptTemplate(
    input_variables=["class_level", "subject", "topic"],
    template="""Generate 10 multiple-choice questions for {class_level} level {subject} on the topic of {topic}. Each question should have 4 options (a, b, c, d) with only one correct answer. The format will be in Markdown:
1. Question text?
    a. Option 1
    b. Option 2
    c. Option 3
    d. Option 4
2. Question text?
    ...
"""
)

# Create a chain with the prompt template and language model
mcq_chain = LLMChain(llm=llm, prompt=mcq_prompt)

def parse_mcqs(mcqs):
    questions = re.split(r'\n\d+\.\s*', mcqs.strip())[1:]
    formatted_questions = []
    for question in questions:
        question_text = re.search(r'^(.*?)\n\s*[a-d]\.', question, re.DOTALL).group(1).strip()
        options = re.findall(r'([a-d])\.\s*(.*?)\s*(?=[a-d]\.|$)', question, re.DOTALL)
        formatted_questions.append((question_text, options))
    return formatted_questions

def display_questions(formatted_questions):
    mcq = mcq_component.MCQComponent(formatted_questions)
    if mcq.render():
        selected_options = mcq.get_selected_options()
        for index, (question_text, options) in enumerate(formatted_questions):
            correct_answer = options[0][1]  # Assuming the first option is correct
            selected_option = selected_options[index]
            if selected_option == correct_answer:
                st.write(f"Question {index+1}: Correct!")
            else:
                st.write(f"Question {index+1}: Wrong. The correct answer is: {correct_answer}")

def main():
    st.title('School Chatbot')

    selected_class = st.selectbox('Select Class', ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th'])
    selected_subject = st.selectbox('Select Subject', ['Math', 'Science', 'History'])

    topic = st.text_input("Enter the topic")
    if topic:
        if st.button('Generate MCQs'):
            mcqs = mcq_chain.run(class_level=selected_class, subject=selected_subject, topic=topic)
            formatted_questions = parse_mcqs(mcqs)
            display_questions(formatted_questions)

if __name__ == "__main__":
    main()

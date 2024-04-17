import streamlit as st

# Create a custom Streamlit component to handle the MCQ questions
class MCQComponent:
    def __init__(self, formatted_questions):
        self.formatted_questions = formatted_questions
        self.selected_options = [None] * len(formatted_questions)

    def render(self):
        with st.form(key='mcq_form'):
            for i, (question_text, options) in enumerate(self.formatted_questions):
                st.markdown(f"**{i+1}. {question_text}**")
                option_texts = [option_text for _, option_text in options]
                self.selected_options[i] = st.radio(f"Select your answer for question {i + 1}:", option_texts, key=f"q{i}")

            submitted = st.form_submit_button("Submit Answers")
            return submitted

    def get_selected_options(self):
        return self.selected_options

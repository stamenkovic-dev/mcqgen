import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
#from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain, callback_handler
from src.mcqgenerator.logger import logging

# loading json file
with open('/Users/predrag/Coding/mcqgen/Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)


#creating a title for the app
st.title("MCQs Creator Application with LangChain")

#creating a form using st.form
with st.form("user_inputs"):
    #File upload
    uploaded_file=st.file_uploader("Upload a PDF or txt file")

    #input fields
    mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=10)

    #subject
    subject=st.text_input("Insert Subject", max_chars=20)

    #quiz tone
    tone=st.text_input("Complexity Level of Questions", max_chars=20, placeholder="Simple")

    #add Button
    button=st.form_submit_button("Create MCQs")

    # Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading ..."):
            try:
                text = read_file(uploaded_file)
                
                # Reset callback handler counts
                callback_handler.total_tokens = 0
                callback_handler.prompt_tokens = 0
                callback_handler.completion_tokens = 0
                callback_handler.total_cost = 0.0
                
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )
                
                # Display token usage and cost information
                st.write(f"Total Tokens: {callback_handler.total_tokens}")
                st.write(f"Prompt Tokens: {callback_handler.prompt_tokens}")
                st.write(f"Completion Tokens: {callback_handler.completion_tokens}")
                st.write(f"Total Cost: ${callback_handler.total_cost:.4f}")

                if isinstance(response, dict):
                    # extract the quiz data from the response
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            # Display the review in a text box as well
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error(f"Error: {str(e)}")

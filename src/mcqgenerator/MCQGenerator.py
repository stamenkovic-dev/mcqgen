import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging
#from langchain.callbacks import get_openai_callback

#importing necessary packages from langchain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks.base import BaseCallbackHandler

# Load environment variables from the .evn file
load_dotenv()

# Accsee the environment variables 
KEY=os.getenv("OPENAI_API_KEY")

# Create a simple callback handler
class TokenCounterCallback(BaseCallbackHandler):
    def __init__(self):
        super().__init__()
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_cost = 0.0
        
    def on_llm_end(self, response, **kwargs):
        self.total_tokens += response.llm_output['token_usage']['total_tokens']
        self.prompt_tokens += response.llm_output['token_usage']['prompt_tokens']
        self.completion_tokens += response.llm_output['token_usage']['completion_tokens']
        # Calculate cost based on gpt-4.0-mini pricing
        self.total_cost += (self.prompt_tokens * 0.00015 + self.completion_tokens * 0.0006) / 1000


# Updated model initialization with callback
callback_handler = TokenCounterCallback()

llm=ChatOpenAI(openai_api_key=KEY, model_name='gpt-4o-mini', temperature=0.5, callbacks=[callback_handler])

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs.
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

# First chain
quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)
# output_key variable use for storing all outputs 

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the questions and give a complete analysis of the quiz. Only use at max 50 words for complexity\
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that is perfectly fits the students abilities.
Quiz_MCQs:
{quiz}

Check from an expert English writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", 'quiz'], template=TEMPLATE2)

# Second chain
review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

# Sequential Chain
generate_evaluate_chain=SequentialChain(
    chains=[quiz_chain, review_chain], 
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
)


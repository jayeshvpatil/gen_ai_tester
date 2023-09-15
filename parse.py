import streamlit as st
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
import os
from patient import PatientList
from langchain.prompts import PromptTemplate

st.title('Gen AI Tester入門')
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Use Gen AI to generate test data. This sample is just testing how you get list in the format you need

model = ChatOpenAI(model='gpt-4')

patient_list = model.predict("Generate a list of 10 fake patient information for testing. Only return the list. Each person should have firstname, lastname and email")
parser = PydanticOutputParser(pydantic_object = PatientList)
prompt = PromptTemplate(template="Answer the user query. \n {format_instructions} \n {query}",
                        input_variables=["query"],
                        partial_variables ={"format_instructions": parser.get_format_instructions()}
                       
                        )
parser_input = prompt.format_prompt(query=patient_list)
model = ChatOpenAI()
output = model.predict(parser_input.to_string())

parsed_patient_list = parser.parse(output)

st.write(parsed_patient_list)













from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import LLMChain
from langchain.evaluation import QAEvalChain
import streamlit as st

def generate_patient_mkting_list(patient_requests):
    system_template_patient_list_agent = """you are marketing analystl.Please provide a sample data based on the user request :"""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template_patient_list_agent)
    human_template_patient_list_agent = "{{text}}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template_patient_list_agent)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(
        llm= ChatOpenAI(model='gpt-4', temperature=1),
        prompt = chat_prompt)

    results=[]

    for patient_request in patient_requests:
        results.append(chain.run({"input": patient_request, "chat_history": []}))

    return results

def generate_patient_requests(n=5) -> list[str]:
    system_template_patient_agent = """ Generate one utterance for marketing analyst who may get requests for a list of {text}. Try to include different cpt codes and patient conditions as part of the request. Include firstname, lastname and email in the request"""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template_patient_agent)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])

    chain = LLMChain(
        llm= ChatOpenAI(model='gpt-4'),
        prompt = chat_prompt
    )
    results = []
    for _ in range(0,n):
        results.append(chain.run("patients"))
    return results

sql_requests = generate_patient_requests()
st.write(sql_requests)

generated_sqls = generate_patient_mkting_list(sql_requests)
st.write(generated_sqls)


llm = ChatOpenAI(model='gpt-4')
predictions =[]
question_answers = []

for i in range(0, len(generated_sqls)):
    q = sql_requests[i]
    a = generated_sqls[i]
    question_answers.append({'question':q, 'answer':a})
    response = llm.predict(f"Generate the response to the question: {q}. Only print the answer")
    predictions.append({"result": {response}})

st.write("Generating Self Evaluation")
eval_chain = QAEvalChain.from_llm(llm)
graded_outputs = eval_chain.evaluate(question_answers,predictions, question_key="question",prediction_key="result", answer_key="answer")
st.table(graded_outputs)
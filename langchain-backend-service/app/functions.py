import os

from app.db import Session, Customer, Review
from app.prompts import QA_PROMPT,system_message,qa_template
from langchain.prompts import PromptTemplate
import json
from langchain_openai import AzureChatOpenAI
from langchain.chains import RetrievalQA
from app.store import get_vectorstore
import requests


def get_customer_info():
    session = Session()
    customers=session.query(Customer).all()
    session.close()
    if customers:
        return  json.dumps([c.to_json() for c in customers])
    else:
        return "Customer not found"




def create_review(review_text: str):
    session = Session()
    review = Review(review=review_text)
    session.add(review)
    session.commit()
    session.close()
    return "Review created"


def ask_vector_db(question: str):
    llm = AzureChatOpenAI(model_name="gpt-35-turbo", temperature=0.3)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=get_vectorstore().as_retriever(),
        chain_type_kwargs={
            "prompt": PromptTemplate(template=qa_template,
            input_variables=["context", "question"])
            },
    )
    result = qa.run(question)
    return result


def search_in_sap_docs(question: str):
    api_url = "https://help.sap.com/http.svc/elasticsearch?area=content&version=&language=en-US&state=PRODUCTION&q={}&transtype=standard,html,pdf,others&product=&to=19&advancedSearch=0&excludeNotSearchable=1"
    # print(f"question:{question}")
    response = requests.get(api_url.format(question))
    if response.status_code==200:
        data=response.json()
        return data["data"]["results"][0]
    else:
        return "error occurred when calling search_from_sap_help_docs"

api_functions = {
    "create_review": create_review,
    "get_customer_info": get_customer_info,
    "ask_vector_db": ask_vector_db,
    "search_in_sap_docs": search_in_sap_docs
}


### Just for initialisation
def create_customers():
    session = Session()

    customers = {
        "Tapstry": 1,
        "Asics": 2
    }

    for name, id in customers.items():
        customer = Customer(name=name, id=id)
        session.add(customer)

    session.commit()
    session.close()

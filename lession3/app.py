from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import AzureOpenAIEmbeddings,AzureChatOpenAI
from langchain_community.vectorstores import FAISS #Chroma
from langchain.chains import RetrievalQA
from openai import AzureOpenAI
import streamlit as st
import time
import os


client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2023-05-15"
)

AZURE_OPENAI_GPT_DEPLOYMENT="gpt-35-turbo"

pdfPath="./IRM Help.pdf"
loader=PyPDFLoader(pdfPath)
pages=loader.load_and_split()

embedding_deployment="text-embedding-ada-002"
embeddings = AzureOpenAIEmbeddings(deployment=embedding_deployment)

if not os.path.exists("faiss_index"):
    db = FAISS.from_documents(pages, embeddings)
    db.save_local("faiss_index")
else:
    db = FAISS.load_local("faiss_index", allow_dangerous_deserialization=True,embeddings=embeddings)

llm = AzureChatOpenAI(model_name="gpt-35-turbo", temperature=0.3)
pdf_qa = RetrievalQA.from_chain_type(llm,
             retriever=db.as_retriever(search_type="similarity_score_threshold",
               search_kwargs={"score_threshold": 0.2}))
# query="manage carriers?"
# result=pdf_qa({"query":query})

# Streamed response emulator
def response_generator(resMessage:str):
    response=pdf_qa({"query":resMessage})
    for word in response["result"].split():
        yield word + " "
        time.sleep(0.05)


st.title("Pdf Similarity Search")

default_message="Total Pdf pages:{}, please type any text to search. eg.manage carriers.".format(len(pages))
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages =  [{"role": "assistant","content":default_message}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter your text to search..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
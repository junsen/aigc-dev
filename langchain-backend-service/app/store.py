from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
from langchain_openai import AzureOpenAIEmbeddings,AzureChatOpenAI
from langchain_community.vectorstores import FAISS #Chroma
from langchain.chains import RetrievalQA
from openai import AzureOpenAI
import os


def create_store():
    pdfPath="./data/IRM Help.pdf"
    loader=PyPDFLoader(pdfPath)
    pages=loader.load_and_split()

    embedding_deployment="text-embedding-ada-002"
    embeddings = AzureOpenAIEmbeddings(deployment=embedding_deployment)
    vectorstore = FAISS.from_documents(pages, embeddings)
    vectorstore.save_local("faiss_index")


def get_vectorstore():
    embedding_deployment="text-embedding-ada-002"
    embeddings = AzureOpenAIEmbeddings(deployment=embedding_deployment)
    vectorstore = FAISS.load_local("faiss_index", allow_dangerous_deserialization=True,embeddings=embeddings)
    return vectorstore



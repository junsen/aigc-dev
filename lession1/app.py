import streamlit as st
import tiktoken
import time

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2023-05-15"
)

AZURE_OPENAI_GPT_DEPLOYMENT="gpt-35-turbo"


# Streamed response emulator
def response_generator(resMessage:str):
    response=resMessage
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Hello World")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages =  [{"role": "assistant","content":"hi"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter your text to chat with chatGPT..."):
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
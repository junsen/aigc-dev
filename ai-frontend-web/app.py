import requests
import json
import streamlit as st
import time
from PIL import Image

st.title("IRM Administrator Assistant")

#opening the image

image = Image.open('./Architecture.png')
st.image(image, caption='architecture')

markdown="""
### Sample questions:
- How to manage brands in IRM?
- How many customers have been onboarded on IRM?
- Write a comment: IRM is great!
- What's Datasphere?
"""
st.markdown(markdown)
chatbox, review=st.columns([6,4])

# defining the api-endpoint
API_ENDPOINT = "http://10.0.0.27:5566/conversation"
DEFAULT_MESSAGE="I am your digital assistant."



# Streamed response emulator
def response_generator(resMessage:str):
    for word in resMessage.split():
        yield word + " "
        time.sleep(0.05)

def conversation(prompt:str):
    payload = {
        "conversation": {
            "messages": [{
                "role": "string",
                "content": "string"
            }]
        },
        "query": prompt
    }
    # sending post request and saving response as response object
    response = requests.post(API_ENDPOINT, json=payload)
    if response.status_code==200:
        return response.json()["response"]
    else:
        return "Error:{}".format(response.status_code)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages =  [{"role": "assistant","content":DEFAULT_MESSAGE}]

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
        response = st.write_stream(response_generator(conversation(prompt)))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


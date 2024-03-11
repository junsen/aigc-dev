import streamlit as st
import tiktoken
import time

messageHeader="The token length for your input is"
default_wiki="""In today's rapidly changing world, knowledge is constantly being refreshed, and it's essential to adapt and evolve in order to avoid becoming obsolete. The impact of macro-economic factors on our company and industry necessitates a proactive approach skill development and strategic influence to ensure that our team remains at the forefront of our organization. By leveraging our collective skills and expertise, we have the opportunity to consolidate efforts across multiple teams and achieve larger, more impactful goals. While individuals may excel in their own right, it's through collaborative efforts that we can truly propel our path forward."""
encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
encodedWiki=encoding.encode(default_wiki)

# Streamed response emulator
def response_generator(resMessage:str):
    response="{} : {} with encoding :{}.".format(messageHeader,len(encoding.encode(resMessage)),encoding)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Count Token Application")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages =  [{"role": "user","content":default_wiki},
                                  {"role": "assistant", "content": "{} : {} with encoding :{}.".format(messageHeader,len(encodedWiki),encoding)}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter your text to calculate token..."):
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
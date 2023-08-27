from lib.api.chat import chat
import time
import streamlit as st

st.markdown("# Your research bot 🤖")

# Initialize chat history
if "botmessages" not in st.session_state:
    st.session_state.botmessages = []
    st.session_state.sourceDocuments = {}
    with st.chat_message("assistant"):
        st.write("Hello 👋. I am your research bot 🤖. Ask me anything in my knowledge base only. If you would like \
             to see my resources, please click on 'Show source documents'.")

# Display chat messages from history on app rerun
for message in st.session_state.botmessages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me anything in my knowledge base"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.botmessages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # call api to get response
        response = chat(prompt, True)
        assistant_response = response["text"]

        st.session_state.sourceDocuments = response['sourceDocuments']
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.botmessages.append(
        {"role": "assistant", "content": full_response})

source = st.checkbox('Show source documents')

if source:
    st.json(st.session_state.sourceDocuments)

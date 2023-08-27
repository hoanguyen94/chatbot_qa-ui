from lib.api.chat import buddyChat
import time
import streamlit as st

st.markdown("# Your research buddy 👩‍🎓")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.intermediateSteps = []
    with st.chat_message("assistant"):
        st.write("Greetings 👋. I am your research buddy 👩‍🎓. Ask me anything. If you would like \
             to see my chain-of-thought, please click on 'Show intermediate steps'.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("Ask me anything in my knowledge base"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # call api to get response
        response = buddyChat(prompt)
        assistant_response = response["output"]

        st.session_state.intermediateSteps = response['intermediateSteps']
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})


source = st.checkbox('Show intermediate steps')

if source:
    st.json(st.session_state.intermediateSteps)

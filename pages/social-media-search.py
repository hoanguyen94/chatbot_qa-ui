import streamlit as st
from lib.api.chat import uploadInfluencer, sqlChat
import pandas as pd
from lib.util.helper import splitChunk
import numpy as np
import time

st.markdown("# Social media research :mortar_board:")


def updateDatabase(df: pd.DataFrame):
    df = df.replace(np.nan, None)
    jsonFile = df.to_dict('records')
    json_chunks = list(splitChunk(jsonFile, 20))
    for chunk in json_chunks:
        response = uploadInfluencer(chunk)
        if response.status_code == 201:
            st.write(
                f"Batch of {len(chunk)} records updated to the database successfully")
        else:
            st.write(
                f"Batch of {len(chunk)} records not updated to the database successfully")
            st.write(f"Error: {response.content}")


def visualize(df: pd.DataFrame):
    st.write(dataframe)
    st.write("Summary statistics")
    st.write(dataframe.describe())

    # columns
    st.header("Visualization")
    cols = tuple(dataframe.columns.values)
    xAxis = st.radio("Select column for x axis",
                     cols, index=3, horizontal=True)
    YAxis = st.radio("Select column for y axis", cols,
                     index=6, horizontal=True)
    st.subheader("Bar chart")

    st.bar_chart(dataframe, x=xAxis, y=YAxis)


action = st.radio("Would you like to", ("upload data", "chat with data"))

if action == "upload data":
    uploaded_file = st.file_uploader("Influencer file :man-surfing:", "csv")

    # show example
    example = pd.DataFrame({'channel': ["youtube", "tiktok"], 'userid': ["samso", "peter123"],
                            'name': ['Sam', 'Peter'], "category1": ["music", "movies"], "category2": ["pop", "cartoon"],
                            "country": ["Germany", "Austria"], "followers": [1000, 5000], "views": [10000, 4000],
                           "likes": [100, 500], "comments": [200, 400]})

    exampleButton = st.checkbox("Show example of CSV file")
    if exampleButton:
        st.write(example)

    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)

        # save to state
        st.session_state.data = uploaded_file
        st.session_state.df = dataframe
        visualize(dataframe)

        updateDB = st.radio(
            "Do you want to update to the database now?", ("Yes", "No"), index=1)
        if updateDB == "Yes":
            st.write(updateDatabase(dataframe))

else:
    # Initialize chat history
    if "sqlChat" not in st.session_state:
        st.session_state.sqlChat = []
        st.session_state.sqlIntermediateSteps = []

    # Display chat messages from history on app rerun
    for message in st.session_state.sqlChat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask me anything in my SQL database"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.sqlChat.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # call api to get response
            response = sqlChat(prompt)
            assistant_response = response["output"]

            st.session_state.sqlIntermediateSteps = response['intermediateSteps']
            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.sqlChat.append(
            {"role": "assistant", "content": full_response})

    source = st.checkbox('Show intermediate steps')

    if source:
        st.json(st.session_state.sqlIntermediateSteps)

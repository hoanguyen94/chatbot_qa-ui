import streamlit as st
from lib.api.chat import postPDF, summarize, summarizeYoutube, extractTopics


st.markdown("# Upload/ Summarize :mortar_board:")


def showIntermediateSteps():
    source = st.checkbox('Show intermediate steps')

    if source:
        st.json(st.session_state.intermediateSteps)


def showTopic(input):
    topicObj = extractTopics(input)
    if isinstance(topicObj, list):
        topics = [t.topic for t in topicObj]
        st.write("Topics: ", ", ".join(topics))
    else:
        st.write("Topic: ", topicObj["topic"])


action = st.radio(
    "Would you like a document :newspaper: to be",
    ('summarized a PDF file', 'summarize a youtube video', 'uploaded to the knowledge base of research buddy and research bot'))

# initialize intermediate steps
if "intermediateSteps" not in st.session_state:
    st.session_state.intermediateSteps = []

if action == "summarized a PDF file":

    uploaded_file = st.file_uploader(
        "Document that needs to be summarized :man-surfing:", "pdf", False)
    if uploaded_file is not None:
        # file = open(uploaded_file, "rb")
        response = summarize(uploaded_file)
        if response.status_code != 201:
            st.write(response.reason)
            if st.checkbox("See error details"):
                st.write(response.content)
        else:
            response = response.json()
            st.session_state.intermediateSteps = response['intermediateSteps']
            showTopic(response['text'])
            st.write(response['text'])
            showIntermediateSteps()


elif action == 'summarize a youtube video':
    link = st.text_input("Enter youtube video link 👇",
                         placeholder="Youtube video link")

    if "https://www.youtube.com" in link:
        response = summarizeYoutube(link)
        if response.status_code != 201:
            st.write(response.reason)
            if st.checkbox("See error details"):
                st.write(response.content)
        else:
            response = response.json()
            st.session_state.intermediateSteps = response['intermediateSteps']
            showTopic(response['text'])
            st.write(response['text'])
            showIntermediateSteps()

else:

    uploaded_file = st.file_uploader(
        "Document to be uploaded to the knowledge base :ski:", "pdf", False)
    if uploaded_file is not None:
        # file = open(uploaded_file, "rb")
        response = postPDF(uploaded_file)
        if response.status_code != 201:
            st.write(response.reason)
            if st.checkbox("See error details"):
                st.write(response.content)
        else:
            st.write(
                "Uploaded successfully :beers:. You can start asking your bot about this document.")
            if st.checkbox("Show full response"):
                st.write(response.json())

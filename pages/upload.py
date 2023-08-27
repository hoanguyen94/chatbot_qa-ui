import streamlit as st
from lib.api.chat import postPDF, summarize


st.markdown("# Upload/ Summarize :mortar_board:")


action = st.radio(
    "Would you like a document :newspaper: to be",
    ('summarized', 'uploaded to the knowledge base of research buddy and research bot'))

if action == "summarized":
    # initialize intermediate steps
    if "intermediateSteps" not in st.session_state:
        st.session_state.intermediateSteps = []

    uploaded_file = st.file_uploader(
        "Document that needs to be summarized :man-surfing:", "pdf", False)
    if uploaded_file is not None:
        # file = open(uploaded_file, "rb")
        response = summarize(uploaded_file)
        st.session_state.intermediateSteps = response['intermediateSteps']
        st.write(response['text'])

    source = st.checkbox('Show intermediate steps')

    if source:
        st.json(st.session_state.intermediateSteps)

else:

    uploaded_file = st.file_uploader(
        "Document to be uploaded to the knowledge base :ski:", "pdf", False)
    if uploaded_file is not None:
        # file = open(uploaded_file, "rb")
        response = postPDF(uploaded_file)
        if response.status_code == 201:
            st.write(
                "Uploaded successfully :beers:. You can start asking your bot about this document.")
            if st.checkbox("Show full response"):
                st.write(response.json())

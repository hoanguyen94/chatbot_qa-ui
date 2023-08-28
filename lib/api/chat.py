import json
import requests
import os
import streamlit as st
import yaml
from dotenv import load_dotenv

load_dotenv()

with open("lib/util/config.yaml", "r") as file:
    config = yaml.safe_load(file)

api_url = os.getenv('CHATURL', config['API']['CHATURL'])


@ st.cache_data
def chat(input: str, source=False) -> json:
    if source:
        full_url = api_url + "/qachat?source=true"
    else:
        full_url = api_url

    response = requests.post(full_url, json={"input": input})
    return response.json()


@ st.cache_data
def buddyChat(input: str) -> json:
    full_url = api_url + "/chatty"
    response = requests.post(full_url, json={"input": input})
    return response.json()


@ st.cache_data
def checkHealth() -> requests.Response:
    full_url = api_url + "/health"
    response = requests.get(full_url)
    return response


# @ st.cache_data
def postPDF(file: file) -> requests.Response:
    full_url = api_url + "/upload-pdf"
    data = {"pdfFile": file}
    response = requests.post(full_url, files=data)
    return response


@ st.cache_data
def summarize(file: file) -> str:
    full_url = api_url + "/summarize?immediateStep=true"
    data = {"paper": file}
    response = requests.post(full_url, files=data)
    return response.json()


@ st.cache_data
def sqlChat(input: str) -> json:
    full_url = api_url + "/sql-chat"
    response = requests.post(full_url, json={"input": input})
    return response.json()

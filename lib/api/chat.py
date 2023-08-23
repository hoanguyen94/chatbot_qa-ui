import requests
import os
import streamlit as st
import yaml

with open("lib/util/config.yaml", "r") as file:
    config = yaml.safe_load(file)

api_url = os.getenv('CHATURL', config['API']['CHATURL'])


@ st.cache_data
def chat(input: str) -> str:
    response = requests.post(api_url, json={"input": input})
    return response.json()["text"]


@ st.cache_data
def checkHealth() -> requests.Response:
    full_url = api_url + "/health"
    response = requests.get(full_url)
    return response


# @ st.cache_data
def postPDF(file: file) -> requests.Response:
    full_url = api_url + "/upload-pdf"
    data = {"file": file}
    response = requests.post(full_url, files=data)
    return response


@ st.cache_data
def summarize(file: file) -> str:
    full_url = api_url + "/summarize"
    data = {"paper": file}
    response = requests.post(full_url, files=data)
    return response.json()["text"]

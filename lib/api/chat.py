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


@ st.cache_data(ttl=60)
def chat(input: str, source=False) -> json:
    try:
        if source:
            full_url = api_url + "/qachat?source=true"
        else:
            full_url = api_url

        response = requests.post(full_url, json={"input": input})
        return response.json()
    except Exception as err:
        raise ConnectionError("API for qa chat is down.") from err


@ st.cache_data(ttl=60)
def buddyChat(input: str) -> json:
    try:
        full_url = api_url + "/chatty"
        response = requests.post(full_url, json={"input": input})
        return response.json()
    except Exception as err:
        raise ConnectionError("API for chat agent is down.") from err


@ st.cache_data(ttl=60)
def checkHealth() -> requests.Response:
    full_url = api_url + "/health"
    response = requests.get(full_url)
    return response


@ st.cache_data(ttl=10)
def postPDF(file: file) -> requests.Response:
    try:
        full_url = api_url + "/upload-pdf"
        data = {"pdfFile": file}
        response = requests.post(full_url, files=data)
        return response
    except Exception as err:
        raise ConnectionError("API to upload pdf file is down.") from err


@ st.cache_data(ttl=60)
def summarize(file: file) -> str:
    try:
        full_url = api_url + "/summarize?intermediateStep=true"
        data = {"paper": file}
        response = requests.post(full_url, files=data)
        return response
    except Exception as err:
        raise ConnectionError("API to summarize is down.") from err


@ st.cache_data(ttl=60)
def sqlChat(input: str) -> json:
    try:
        full_url = api_url + "/sql-chat"
        response = requests.post(full_url, json={"input": input})
        return response.json()
    except Exception as err:
        raise ConnectionError("API for sql chat is down.") from err


@ st.cache_data(ttl=60)
def summarizeYoutube(link: str, chunkSize=2000):
    try:
        full_url = api_url + "/summarize-youtube?intermediateStep=True"
        json = {
            "link": link,
            "chunkSize": chunkSize
        }
        response = requests.post(full_url, json=json)
        return response
    except Exception as err:
        raise ConnectionError(
            "API to summarize youtube video is down.") from err


@ st.cache_data(ttl=60)
def extractTopics(input: str):
    try:
        full_url = api_url + "/extract-topic"
        json = {
            "input": input,
        }
        response = requests.post(full_url, json=json)
        return response.json()
    except Exception as err:
        raise ConnectionError("API to extract topics is down.") from err

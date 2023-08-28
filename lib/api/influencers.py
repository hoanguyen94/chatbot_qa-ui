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
def uploadInfluencer(file: json) -> requests.Response:
    full_url = api_url + "/influencer"
    response = requests.post(full_url, json=file)
    return response


@ st.cache_data
def getAllInfluencer() -> requests.Response:
    full_url = api_url + "/influencer"
    response = requests.get(full_url)
    return response


@ st.cache_data
def delAllInfluencer() -> requests.Response:
    full_url = api_url + "/influencer"
    response = requests.delete(full_url)
    return response

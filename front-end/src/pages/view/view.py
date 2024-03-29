import streamlit as st
import pandas as pd
import requests
import json

def view():
  url = 'http://34.73.83.102:8001/get_data'
  payload = {"token": st.session_state["token"]}
  json_data = json.dumps(payload)
  headers = {
    'Content-Type': 'application/json',
  }
  response = requests.post(url, headers=headers, data=json_data)
  if response.status_code == 200:
    st.wtite("hi")
  else:
    st.write("bye")

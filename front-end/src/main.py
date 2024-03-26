import streamlit as st
from auth_pages.auth_page import menu_login

st.set_page_config(page_title='Streamlit App', page_icon='🤧')

menu_login()


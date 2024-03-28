import streamlit as st
from streamlit_option_menu import option_menu
from pages.upload.file_upload import file_uploader

def tabs():
  if st.session_state["role"] == "Admin":
    options = ["Upload", "View", "Manage", "Account"]
    icons = ['cloud-upload-fill','clipboard-data-fill', 'gear-fill', 'person-fill'] 
  else:
    options = ["Upload", "View", "Account"]
    icons = ['cloud-upload-fill','clipboard-data-fill', 'person-fill'] 
  
  login_menu = option_menu(None, options, 
    icons=icons, 
    menu_icon="cast", 
    key='nav_menu',
    default_index=0, 
    orientation="horizontal"
  )
  
  login_menu
  
  if st.session_state["nav_menu"] == "Upload" or st.session_state["nav_menu"] == None:
    file_uploader()
  elif st.session_state["nav_menu"] == "View":
    st.write("v")
  elif st.session_state["nav_menu"] == "Account":
    st.write("A")
  elif st.session_state["nav_menu"] == "Manage":
    st.write("M")

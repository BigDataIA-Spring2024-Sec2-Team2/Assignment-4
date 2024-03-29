import streamlit as st

def file_uploader():
  with st.form(key='upload', clear_on_submit=True):
    uploaded_file = st.file_uploader("Choose a PDF file to Extract and load data", type=["pdf"], accept_multiple_files=False, key="file_upload")
    
    btn1, btn2, btn3 = st.columns([4, 2, 4])
  
    with btn2:
      sub = st.form_submit_button("Upload file")
    
  if sub:  
    if uploaded_file:
      # TODO: link to the API serice 
      st.success("File Uploaded")
    else:
      st.error("Please select a file before uploading")
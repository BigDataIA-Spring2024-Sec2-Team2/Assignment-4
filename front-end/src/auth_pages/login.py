import streamlit as st

def login():
  with st.form(key='login', clear_on_submit=False):
    st.subheader(':red[Login]')
    username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
    password = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
    btn1, btn2, btn3 = st.columns([3, 1, 3])
    with btn2:
      sub = st.form_submit_button('Login')
      
    if sub:
      if validate_username(username) and validate_password(password):
        pass
      
def validate_username(username):
  if username:
    return True
  else:
    st.warning('Enter an Username')
    return False

def validate_password(password):
  if password:
    return True
  else:
    st.warning('Enter Password')
    return False
import streamlit as st
import re

def sign_up():
  with st.form(key='signup', clear_on_submit=True):
    st.subheader(':red[Sign Up]')
    email = st.text_input(':blue[Email]', placeholder='Enter Your Email')
    username = st.text_input(':blue[Username]', placeholder='Enter Your Username')
    password1 = st.text_input(':blue[Password]', placeholder='Enter Your Password', type='password')
    password2 = st.text_input(':blue[Confirm Password]', placeholder='Confirm Your Password', type='password')
    btn1, btn2, btn3 = st.columns([3, 1, 3])

    with btn2:
      sub = st.form_submit_button('Sign Up')

    if sub:
      if validate_email(email) and validate_username(username) and validate_password(password1, password2):
        # TODO call the create new user service
        pass

def validate_email(email):
  # Regular expression for email validation
  regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
  if email:
    if re.match(regex, email):
      return True
    else:
      st.warning('Invalid Email')
      return False
  else:
    st.warning('Enter an Email')
    return False

def validate_username(username):
  if username:
    if len(username) > 3:
      return True
    else:
      st.warning('Invalid Username')
      return False
  else:
    st.warning('Enter an Username')
    return False

def validate_password(password1, password2):
  if password1:
    if password2:
      if password1 == password2:
        return True
      else:
        st.warning("Password Don't Match")
        return False
    else:
      st.warning('Enter Confirm Password')
      return False
  else:
    st.warning('Enter Password')
    return False
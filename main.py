import os
import streamlit as st
from components import Session, SessionManager, add_user_modal

st.set_page_config(
    page_title="Workbench",
    page_icon=":hammer:",
    initial_sidebar_state='collapsed',
    layout='wide'
)
if st.session_state.get("username") is None:
    st.session_state.username = SessionManager.get_username()
    if st.session_state.username is None:
        add_user_modal()

if st.session_state.get("session") is None and st.session_state.username is not None:
    st.session_state.session = Session(user=st.session_state.username)
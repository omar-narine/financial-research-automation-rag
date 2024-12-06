import streamlit as st

st.set_page_config(page_title="Financial Analysis with LLMs")

if 'query' not in st.session_state:
    st.session_state.query = ''

st.title("Financial Analysis with LLMs & RAG")

st.subheader("Please enter a search query to get started!")

st.text_input(
    label = "How can I ",
    value=st.session_state.repo_url,
    disabled=False,
    key="repo_url",
    on_change=on_repo_url_change
)




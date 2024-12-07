import streamlit as st

from functions.query_calls import query_rag

st.set_page_config(page_title="Financial Analysis with LLMs")

if 'query' not in st.session_state:
    st.session_state.query = ''

st.title("Financial Analysis with LLMs & RAG")

st.subheader("Please enter a search query to get started: ")


def on_query_change():
    rag_response, top_matches = query_rag(st.session_state.query)

    st.markdown(rag_response)


st.text_input(
    label="What can I help you with today?",
    value=st.session_state.query,
    disabled=False,
    key="query",
    on_change=on_query_change
)


col1, col2, col3 = st.columns(3)

with col1:
    st.write("Column 1")

with col2:
    st.write("Column 2")

with col3:
    st.write("Column 3")

import streamlit as st
import requests
import plotly.graph_objects as go
# from functions.query_calls import query_rag

st.set_page_config(page_title="Financial Analysis with LLMs")

if 'query' not in st.session_state:
    st.session_state.query = ''

if 'tickers' not in st.session_state:
    st.session_state.tickers = []

if 'top_matches' not in st.session_state:
    st.session_state.top_matches = []

st.title("Financial Analysis with LLMs & RAG")

st.subheader("Please enter a search query to get started: ")


def on_query_change():

    def query_rag(query):
        url = "http://127.0.0.1:5000/query"
        params = {"query": query}
        response = requests.get(url, json=params)

        return response.json()

    query_response = query_rag(st.session_state.query)
    rag_response = query_response.get('response')
    top_matches = query_response.get('stocks')

    st.session_state.top_matches = top_matches

    st.session_state.tickers = [match['Ticker']
                                for match in top_matches]

    st.markdown(rag_response)
    st.write(st.session_state.tickers)
    # st.write(len(top_matches))


st.text_input(
    label="What can I help you with today?",
    value=st.session_state.query,
    disabled=False,
    key="query",
    on_change=on_query_change
)

if st.session_state.tickers:
    stock_info_tabs = st.tabs(st.session_state.tickers)


def get_fear_and_greed():
    url = "http://127.0.0.1:5000/current-fear-and-greed"
    response = requests.get(url)
    return response.json()


def create_gauge_chart(value):
    # Define the colors and ranges for the gauge
    colors = ['#FF4136', '#FF851B', '#FFDC00', '#01FF70', '#2ECC40']

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value['value'],
        title={'text': f"Fear & Greed Index: {value['value_classification']}", 'font': {
            'size': 24}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 20], 'color': '#FF4136'},    # Extreme Fear
                {'range': [20, 40], 'color': '#FF851B'},   # Fear
                {'range': [40, 60], 'color': '#FFDC00'},   # Neutral
                {'range': [60, 80], 'color': '#01FF70'},   # Greed
                {'range': [80, 100], 'color': '#2ECC40'}   # Extreme Greed
            ],
        }
    ))

    fig.update_layout(
        height=400,
        font={'color': "darkblue", 'family': "Arial"}
    )

    return fig


# Add this after your existing code, perhaps in a sidebar or new container
with st.container():
    st.subheader("Market Fear & Greed Index")
    try:
        fgi_data = get_fear_and_greed()
        fig = create_gauge_chart(fgi_data)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Unable to load Fear & Greed Index: {str(e)}")

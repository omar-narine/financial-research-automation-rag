from sentence_transformers import SentenceTransformer
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone
import os
from openai import OpenAI
from pathlib import Path
from langchain.schema import Document
from pinecone import Pinecone

# API Dependencies/Imports
import pickle
import numpy as np
from flask import Flask, request, Response
import json
from script.get_news import get_news
from script.fear_and_greed import get_fgi

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"

    '''
    I want this api call to process any incoming query request and it the body of the response, there should be a list of stocks that are mentioned in the rag response. 
    These stocks should be formatted in a dictionary format with the stock ticker or name (depending on what is used on the pinecone db, I have to double check). 

    The streamlit app will then parse these stocks and display their information in some sort of container. If I have time, I'd like to try and make it so that they they can also be used to find some news information regarding those stocks as well.
    '''


@app.route('/query', methods=["GET"])
def process_query():

    data = request.get_json()
    query = data.get('query')

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    pinecone_index = pc.Index("stocks")

    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY")
    )

    def get_huggingface_embeddings(text, model_name="sentence-transformers/all-mpnet-base-v2"):
        model = SentenceTransformer(model_name)
        return model.encode(text)

    def perform_rag(query):
        raw_query_embedding = get_huggingface_embeddings(query)

        top_matches = pinecone_index.query(vector=raw_query_embedding.tolist(
        ), top_k=10, include_metadata=True, namespace='stock-descriptions-new')

        # Get the list of retrieved texts
        contexts = [item['metadata']['text']
                    for item in top_matches['matches']]

        augmented_query = "<CONTEXT>\n" + "\n\n-------\n\n".join(
            contexts[: 10]) + "\n-------\n</CONTEXT>\n\n\n\nMY QUESTION:\n" + query

        # Modify the prompt below as need to improve the response quality
        system_prompt_old = f"""You are a financial analyst with a broad scope of knowledge regarding the stock market. You are currently responsible for a new team of traders who will be handling a lot of money for the company and your clients. These new traders have a lot of questions about the stock market, the stocks, and overall financial analysis. They need your help in order to answer these questions and learn so that they have the the best set of tools and knowledge in order to maximize their returns. 
        
        When they are asking their questions, some high level context will be provided including stocks that are relevant to their question. Using this context, you should provide a response that is both accurate and helpful to the question asked. You want to be clear and direct in your response. Please ensure that you are not explicitly mentioning the contents of the context you are being given, but rather use it to formulate your response. The actual stocks should be acknowledged in your response and included in the response. 
               
        The scope of your response should be limited to the context provided. You should not mention any stocks outside of the context provided. Please do not mention any stocks that are not in the context provided.
        """

        system_prompt = '''
        You are a financial analyst at a large trading firm with a lot of knowledge relating to the stock market. You are being asked to answer some questions from a new and upcoming trader. 
        
        Using the context provided, answer the traders question, being sure to explain all of the stocks provided in the context and how they might answer the question being posed. Please limit your inclusion of stocks outside of the provided context to prevent confusion for the trader.
        
        Please include ALL OF THE STOCKS provided in the context in your response. 
        '''

        llm_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": augmented_query}
            ]
        )

        top_matches_formatted = [item['metadata']
                                 for item in top_matches["matches"]]

        return llm_response.choices[0].message.content, top_matches_formatted

    try:
        rag_response, top_matches = perform_rag(query)

        json_msg = {
            "response": rag_response,
            "stocks": top_matches,
            "message": "RAG Response Successful",
            "status": 200
        }

        return Response(json.dumps(json_msg), status=200, mimetype='application/json')

    except Exception as e:
        print(e)

        json_msg = {
            "response": f"An error occurred: {e}",
            "message": "Internal Server Error - RAG Response Failed",
            "status": 500
        }
        return Response(json.dumps(json_msg), status=500, mimetype='application/json')


@app.route('/stock-news', methods=["GET"])
def get_stock_news():
    data = request.get_json()
    ticker = data.get('ticker')
    stock_name = data.get('stock_name')

    news = get_news(ticker, stock_name)

    return Response(json.dumps(news), status=200, mimetype='application/json')


@app.route('/current-fear-and-greed', methods=["GET"])
def get_fear_and_greed():

    try:
        fg_index = json.loads(get_fgi())

        current_fg_index = (fg_index.get('fgi').get('now'))

        return Response(json.dumps(current_fg_index), status=200, mimetype='application/json')

    except Exception as e:
        json_msg = {
            "response": f"An error occurred: {e}",
            "message": "Internal Server Error - FGI Response Failed",
            "status": 500
        }
        return Response(json.dumps(json_msg), status=500, mimetype='application/json')


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request, jsonify
import os
from langchain_openai import OpenAIEmbeddings
from langchain.chains.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from openc import OpenCC
import openai
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_response():
    user_input = request.form.get('user_input')
    db = None
    if not user_input:
        return jsonify({'error': 'No user input provided'})
    if user_input:
        embeddings = OpenAIEmbeddings()
        db = Chroma(persist_directory="./db/temp/", embedding_function=embeddings)
        docs = db.similarity_search(user_input)
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0.5)
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.invoke({"input_documents": docs, "question": user_input}, return_only_outputs=True)
        cc = OpenCC('s2t')
        answer = cc.convert(response['output_text'])
        chat_history.append({'user': user_input, 'assistant': response['output_text']})
        return jsonify({'response': answer})

from flask import Flask, request, jsonify
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from opencc import OpenCC
import openai
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 初始化 Flask 應用程式
app = Flask(__name__)

# OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/api/get_response', methods=['POST'])
def get_response():
    # 取得用戶輸入
    user_input = request.form.get('user_input')
    if not user_input:
        return jsonify({'error': 'No user input provided'})

    # 初始化資料庫
    db = None
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory="./db/temp/", embedding_function=embeddings)
    
    # 搜索相似文檔
    docs = db.similarity_search(user_input)
    
    # 初始化 LLM 和 QA 鏈
    llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=0.5
    )
    chain = load_qa_chain(llm, chain_type="stuff")

    # 呼叫 OpenAI API
    with get_openai_callback() as cb:
        response = chain.invoke({"input_documents": docs, "question": user_input}, return_only_outputs=True)

    # 簡繁轉換
    cc = OpenCC('s2t')
    answer = cc.convert(response['output_text'])

    # 返回回答
    return jsonify({'response': answer})

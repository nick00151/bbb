from flask import Flask, request, jsonify
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from opencc import OpenCC
from dotenv import load_dotenv

# 初始化環境
load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

# 初始化 OpenCC
cc = OpenCC('s2t')  # 簡體轉繁體

@app.route("/api/get_response", methods=["POST"])
def get_response():
    data = request.get_json()  # 從 JSON 提取用戶輸入
    user_input = data.get('user_input')

    if not user_input:
        return jsonify({'error': 'No user input provided'}), 400

    try:
        # 加載嵌入和向量數據庫
        embeddings = OpenAIEmbeddings()
        db = Chroma(persist_directory="./db/temp/", embedding_function=embeddings)
        
        # 相似性搜索
        docs = db.similarity_search(user_input)
        
        # 加載模型和 QA chain
        llm = ChatOpenAI(model_name="gpt-4", temperature=0.5)
        chain = load_qa_chain(llm, chain_type="stuff")
        
        # 使用回調處理計算
        with get_openai_callback() as cb:
            response = chain.run({"input_documents": docs, "question": user_input})
        
        # 簡體轉繁體
        answer = cc.convert(response)
        
        return jsonify({'response': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from opencc import OpenCC
import openai
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 設定 OpenAI API 金鑰
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form.get('user_input')
    if not user_input:
        return jsonify({'error': 'No user input provided'})

    # 初始化資料庫和嵌入
    embeddings = OpenAIEmbeddings()
    if not os.path.exists("./db/temp/"):
        os.makedirs("./db/temp/")
    db = Chroma(persist_directory="./db/temp/", embedding_function=embeddings)

    # 搜索相似文件
    docs = db.similarity_search(user_input)

    # 初始化語言模型和 QA 鏈
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.5)
    chain = load_qa_chain(llm, chain_type="stuff")

    try:
        with get_openai_callback() as cb:
            response = chain({"input_documents": docs, "question": user_input})
        if "output_text" not in response:
            return jsonify({'error': 'No output text in response'})

        # 簡繁轉換
        cc = OpenCC('s2t')
        answer = cc.convert(response['output_text'])

        return jsonify({'response': answer})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)

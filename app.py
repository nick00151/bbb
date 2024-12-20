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

app = Flask(__name__, static_folder='static', template_folder='templates')

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/api/get_response', methods=['POST'])
def get_response():
    try:
        data = request.get_json()  # 接收 JSON 資料
        user_input = data.get('user_input')
        if not user_input:
            return jsonify({'error': 'No user input provided'})

        # 初始化 Embeddings 和 Chroma 資料庫
        embeddings = OpenAIEmbeddings()
        if not os.path.exists("./db/temp/"):
            os.makedirs("./db/temp/")
        db = Chroma(persist_directory="./db/temp/", embedding_function=embeddings)

        # 檢索相似文檔
        docs = db.similarity_search(user_input)
        if not docs:  # 如果沒有檢索到任何相關文檔
            return jsonify({'response': '很抱歉，無法找到相關的資料，請嘗試其他問題！'})

        # 啟用 LangChain 的 QA Chain
        llm = ChatOpenAI(model_name="gpt-4", temperature=0.5)
        chain = load_qa_chain(llm, chain_type="stuff")

        # 生成回答
        with get_openai_callback() as cb:
            response = chain({"input_documents": docs, "question": user_input})

        print("Chain response:", response)  # 除錯用
        if "output_text" not in response:  # 如果沒有生成有效回應
            return jsonify({'response': '很抱歉，無法生成答案，請稍後再試！'})

        # 繁簡轉換
        cc = OpenCC('s2t')
        answer = cc.convert(response['output_text'])

        return jsonify({'response': answer})
    except Exception as e:
        print("Error:", str(e))  # 印出錯誤訊息供排查
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)


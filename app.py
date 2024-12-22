from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from opencc import OpenCC
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # 啟用 CORS 支援

openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("未找到 OPENAI_API_KEY，請確認 .env 文件是否正確配置！")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_response', methods=['POST'])
def get_response():
    try:
        data = request.get_json()
        user_input = data.get('user_input')
        if not user_input:
            return jsonify({'response': '請輸入問題，才能獲取回答！'})

        # 確保資料庫目錄存在
        db_path = "./db/temp/"
        if not os.path.exists(db_path):
            return jsonify({'response': '資料庫未初始化，請先建立資料庫！'})

        embeddings = OpenAIEmbeddings()
        db = Chroma(persist_directory=db_path, embedding_function=embeddings)

        # 搜索文件
        docs = db.similarity_search(user_input, k=3)
        if not docs:
            return jsonify({'response': '很抱歉，無法找到相關資料，請換個問題試試！'})

        llm = ChatOpenAI(model_name="gpt-4", temperature=0)
        chain = load_qa_chain(llm, chain_type="stuff")

        with get_openai_callback() as cb:
            response = chain({"input_documents": docs, "question": user_input})

        if not response or "output_text" not in response or not response["output_text"].strip():
            return jsonify({'response': '很抱歉，目前無法生成有效回答，請稍後再試。'})

        # 使用 OpenCC 進行繁體轉換
        cc = OpenCC('s2t')
        answer = cc.convert(response['output_text'])

        return jsonify({'response': answer})

    except Exception as e:
        app.logger.error("發生錯誤：%s", str(e))
        return jsonify({'response': f'發生錯誤：{str(e)}'})

if __name__ == "__main__":
    app.run(debug=True)

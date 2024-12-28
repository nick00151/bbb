from flask import Flask, render_template, request, jsonify # 引入所需模組
import os # 用於操作系統功能
from langchain.embeddings.openai import OpenAIEmbeddings # 生成向量嵌入
from langchain.chains.question_answering import load_qa_chain # 載入問答鏈
from langchain.callbacks import get_openai_callback # 用於監控請求
from opencc import OpenCC # 用於簡繁轉換
import openai # OpenAI API
from langchain.chat_models import ChatOpenAI # 使用 ChatGPT 模型
from langchain.vectorstores import Chroma # 向量存儲
from dotenv import load_dotenv # 加載環境變數

load_dotenv() # 加載 .env 文件

app = Flask(__name__, static_folder='static', template_folder='templates') # 初始化 Flask 應用

openai.api_key = os.getenv('OPENAI_API_KEY') # 獲取 OpenAI API 密鑰

@app.route('/')
def index():
    return render_template('index.html') # 渲染首頁模板

@app.route('/api/get_response', methods=['POST'])
def get_response():
    try:
        data = request.get_json() # 獲取前端的 JSON 數據
        user_input = data.get('user_input') # 提取用戶輸入
        if not user_input: # 如果未提供輸入
            return jsonify({'response': '請輸入問題，才能獲取回答！'})

        embeddings = OpenAIEmbeddings() # 創建向量嵌入對象
        if not os.path.exists("./db/temp/"): # 如果向量存儲目錄不存在
            os.makedirs("./db/temp/") # 創建目錄
        db = Chroma(persist_directory="./db/temp/", embedding_function=embeddings) # 初始化向量存儲

        docs = db.similarity_search(user_input, k=3) # 搜索與問題相關的文件，返回最多 3 個
        if not docs: # 如果找不到相關文件
            return jsonify({'response': '很抱歉，無法找到相關資料，請換個問題試試！'})

        llm = ChatOpenAI(model_name="gpt-4", temperature=0) # 創建 GPT-4 模型
        chain = load_qa_chain(llm, chain_type="stuff") # 加載問答鏈

        with get_openai_callback() as cb: # 監控 API 調用
            response = chain({"input_documents": docs, "question": user_input}) # 生成回答

        if not response or "output_text" not in response or not response["output_text"].strip(): # 回答無效
            return jsonify({'response': '很抱歉，目前無法生成有效回答，請稍後再試。'})

        try:
            cc = OpenCC('s2t') # 初始化簡體到繁體轉換器
            answer = cc.convert(response['output_text']) # 將回答轉為繁體中文
        except Exception:
            answer = response['output_text'] # 如果轉換失敗，使用原始回答

        return jsonify({'response': answer}) # 返回回答

    except Exception as e: # 捕捉任何異常
        return jsonify({'response': f'發生錯誤：{str(e)}'}) # 返回錯誤訊息

if __name__ == "__main__":
    app.run(debug=True) # 啟動應用




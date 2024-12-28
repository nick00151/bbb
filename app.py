from flask import Flask, render_template, request, jsonify  # 引入 Flask 模組，實現後端伺服器功能
import os  # 提供與作業系統交互的功能，例如檔案和環境變數管理
from langchain.embeddings.openai import OpenAIEmbeddings  # 用於生成基於 OpenAI 的文本嵌入向量
from langchain.chains.question_answering import load_qa_chain  # 加載問答流程的核心處理邏輯
from langchain.callbacks import get_openai_callback  # 用於監控和調試 OpenAI 的回調
from opencc import OpenCC  # 用於繁體和簡體中文的相互轉換
import openai  # OpenAI 的官方 Python SDK，用於與 GPT 模型交互
from langchain.chat_models import ChatOpenAI  # 提供 OpenAI 聊天模型的高層封裝
from langchain.vectorstores import Chroma  # 用於嵌入式資料儲存和檢索
from dotenv import load_dotenv  # 自動讀取 .env 檔案中的環境變數，例如 API 密鑰

# 加載 .env 檔案中的環境變數，尤其是 OpenAI API 密鑰
load_dotenv()

# 初始化 Flask 應用程式，設定靜態檔案和模板目錄
app = Flask(__name__, static_folder='static', template_folder='templates')

# 從環境變數中獲取 OpenAI API 密鑰
openai.api_key = os.getenv('OPENAI_API_KEY')

# 定義首頁路由，返回 HTML 模板 index.html
@app.route('/')
def index():
    return render_template('index.html')  # 渲染首頁 HTML 模板，提供前端界面

# 定義後端 API 路由，處理前端的問題請求並返回回答
@app.route('/api/get_response', methods=['POST'])
def get_response():
    try:
        # 獲取前端發送的 JSON 數據
        data = request.get_json()
        user_input = data.get('user_input')  # 獲取使用者輸入的問題文本
        if not user_input:  # 如果沒有輸入內容，返回錯誤提示
            return jsonify({'response': '請輸入問題，才能獲取回答！'})

        # 初始化嵌入向量生成器
        embeddings = OpenAIEmbeddings()
        
        # 如果臨時資料庫目錄不存在，則創建該目錄
        if not os.path.exists("./db/temp/"):
            os.makedirs("./db/temp/")
        
        # 加載或創建嵌入向量資料庫，存儲相關文本的向量化數據
        db = Chroma(persist_directory="./db/temp/", embedding_function=embeddings)

        # 在資料庫中進行相似性搜索，返回與使用者問題相關的文檔
        docs = db.similarity_search(user_input, k=3)  # 限制最多返回 3 個相關文檔
        if not docs:  # 如果找不到相關文檔，返回錯誤提示
            return jsonify({'response': '很抱歉，無法找到相關資料，請換個問題試試！'})

        # 初始化聊天模型，指定模型名稱和溫度參數
        llm = ChatOpenAI(model_name="gpt-4", temperature=0)
        
        # 加載問答鏈，使用 "stuff" 模式來生成回答
        chain = load_qa_chain(llm, chain_type="stuff")

        # 使用問答鏈生成回答，並監控 OpenAI 的 API 回調
        with get_openai_callback() as cb:
            response = chain({"input_documents": docs, "question": user_input})

        # 如果回應無效或為空，返回錯誤提示
        if not response or "output_text" not in response or not response["output_text"].strip():
            return jsonify({'response': '很抱歉，目前無法生成有效回答，請稍後再試。'})

        # 將回答轉換為繁體中文，處理潛在的格式化錯誤
        try:
            cc = OpenCC('s2t')  # 使用 OpenCC 進行繁簡轉換
            answer = cc.convert(response['output_text'])  # 將回答從簡體轉換為繁體
        except Exception:
            answer = response['output_text']  # 如果轉換失敗，使用原始簡體回答

        # 返回回答給前端
        return jsonify({'response': answer})

    except Exception as e:  # 處理任意異常，返回錯誤信息
        return jsonify({'response': f'發生錯誤：{str(e)}'})

# 啟動 Flask 伺服器，進入調試模式
if __name__ == "__main__":
    app.run(debug=True)





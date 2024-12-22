@app.route('/api/get_response', methods=['POST'])
def get_response():
    try:
        data = request.get_json()
        user_input = data.get('user_input')

        if not user_input:
            return jsonify({'response': '請輸入問題，才能獲取回答！'}), 400  # 返回 400 錯誤

        # 建立嵌入
        embeddings = OpenAIEmbeddings()

        # 確保資料庫目錄存在
        if not os.path.exists("./db/temp/"):
            os.makedirs("./db/temp/")
        
        # 初始化 Chroma 資料庫
        db = Chroma(persist_directory="./db/temp/", embedding_function=embeddings)

        # 搜索相關文件
        docs = db.similarity_search(user_input, k=3)  # 限制最多返回3個相關文件
        if not docs:
            return jsonify({'response': '很抱歉，無法找到相關資料，請換個問題試試！'}), 404  # 返回 404 錯誤

        # 建立回答生成鏈
        llm = ChatOpenAI(model_name="gpt-4", temperature=0)
        chain = load_qa_chain(llm, chain_type="stuff")

        # 生成回答
        with get_openai_callback() as cb:
            response = chain({"input_documents": docs, "question": user_input})

        # 檢查回答是否有效
        if not response or "output_text" not in response or not response["output_text"].strip():
            return jsonify({'response': '很抱歉，目前無法生成有效回答，請稍後再試。'}), 500  # 返回 500 錯誤

        # 將回答轉換為繁體中文
        try:
            cc = OpenCC('s2t')
            answer = cc.convert(response['output_text'])
        except Exception:
            answer = response['output_text']  # 若繁體轉換失敗，使用原始回答

        return jsonify({'response': answer}), 200

    except Exception as e:
        return jsonify({'response': f'伺服器錯誤：{str(e)}'}), 500  # 返回 500 錯誤


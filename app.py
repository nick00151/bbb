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

@app.route('/')
def index():
    return render_template('index.html')  # 渲染首頁

@app.route('/api/get_response', methods=['POST'])
def get_response():
    try:
        data = request.get_json()
        user_input = data.get('user_input')
        if not user_input:
            return jsonify({'error': 'No user input provided'})

        embeddings = OpenAIEmbeddings()
        if not os.path.exists("./db/temp/"):
            os.makedirs("./db/temp/")
        db = Chroma(persist_directory="./db/temp/", embedding_function=embeddings)

        docs = db.similarity_search(user_input)

        llm = ChatOpenAI(model_name="gpt-4", temperature=0.5)
        chain = load_qa_chain(llm, chain_type="stuff")

        with get_openai_callback() as cb:
            response = chain({"input_documents": docs, "question": user_input})
        if "output_text" not in response:
            return jsonify({'error': 'No output text in response'})

        cc = OpenCC('s2t')
        answer = cc.convert(response['output_text'])

        return jsonify({'response': answer})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)


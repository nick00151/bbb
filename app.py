from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # 需要正確縮排

@app.route('/hello', methods=['POST'])
def hello():
    return jsonify(message='Hello World!')  # 需要正確縮排

if __name__ == '__main__':
    app.run(debug=True)  # 需要正確縮排


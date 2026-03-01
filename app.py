import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')  # 从环境变量读取 API Key
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

@app.route('/ask', methods=['GET'])
def ask_gemini():
    # 从请求参数获取问题，默认问“你好”
    question = request.args.get('q', '你好')
    
    # 构造 Gemini 要求的请求体
    payload = {
        "contents": [{
            "parts": [{"text": question}]
        }]
    }
    
    # 调用 Gemini API
    response = requests.post(GEMINI_URL, json=payload)
    
    # 返回 Gemini 的回答
    if response.status_code == 200:
        result = response.json()
        answer = result['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"question": question, "answer": answer})
    else:
        return jsonify({"error": "调用 Gemini 失败", "details": response.text}), 500

@app.route('/')
def home():
    return "服务已启动！访问 /ask?q=你的问题 即可测试。"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

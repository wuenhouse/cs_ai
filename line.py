from flask import Flask, request, jsonify
import requests
import os
import time
import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from customer_service_ai import CustomerServiceAI

load_dotenv()

app = Flask(__name__)

# LINE Messaging API的設置
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESSTOKEN")
LINE_API_URL = 'https://api.line.me/v2/bot/message/reply'

def initialize_llm():
    return ChatOpenAI(model="gpt-4o")

def initialize_customer_service():
    llm = initialize_llm()

    # 預設 Q&A 資料
    default_qa = []

    # 檢查是否有 Q&A 檔案
    qa_file = "customer_service_qa.json"
    if os.path.exists(qa_file):
        return CustomerServiceAI(llm, qa_file=qa_file)
    else:
        return CustomerServiceAI(llm, qa_data=default_qa)

@app.route('/webhook', methods=['POST'])
def webhook():
    body = request.json
    events = body.get('events', [])

    for event in events:
        if event['type'] == 'message' and event['message']['type'] == 'text':
            user_message = event['message']['text']
            reply_token = event['replyToken']

            # 將用戶消息發送到Streamlit應用
            response = handle_user_message(user_message)

            # 回覆用戶
            reply_message(reply_token, response)

    return jsonify({'status': 'ok'})

def handle_user_message(message):
    # 在這裡調用您的Streamlit應用的邏輯
    # 例如，將消息傳遞給客服助手
    # 這裡可以返回助手的回應
    cs_assistant = initialize_customer_service()
    assistant_response = cs_assistant.answer_question(message, debug_callback=None)
    return assistant_response

def reply_message(reply_token, message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}',
    }
    payload = {
        'replyToken': reply_token,
        'messages': [{'type': 'text', 'text': message}],
    }
    response = requests.post(LINE_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Error sending message. Status code: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    app.run(port=5000)

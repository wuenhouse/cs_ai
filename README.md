# 客服 AI 助手

一個基於 OpenAI 和 LangChain 的智能客服系統，能夠回答常見問題並提供專業的客服支援。

## 功能特點

- 🤖 基於 OpenAI GPT 模型的智能對話系統
- 💬 自然語言處理，準確理解用戶意圖
- 📚 支援從 JSON 和 Word 文件導入 Q&A 知識庫
- 🔍 向量搜索和關鍵詞匹配，提供精確答案
- 📊 調試模式，幫助優化回答質量

## 快速開始

### 安裝依賴

```bash
pip install -r requirements.txt
```

### 設置環境變數

創建 `.env` 文件並添加您的 OpenAI API 密鑰：

```
OPENAI_API_KEY=your_api_key_here
```

### 運行應用

```bash
streamlit run app.py
```

## 知識庫管理

系統支援兩種方式導入 Q&A 知識：

1. **JSON 格式**：結構化的問答對
2. **Word 文件**：自動解析 Q/A 格式的文檔

### JSON 格式範例

```json
[
  {
    "question": "背包禮物怎麼獲得？",
    "answer": "背包禮物可以通過完成每日任務獲得。"
  },
  {
    "question": "如何聯繫客服？",
    "answer": "您可以通過應用內的「聯繫我們」按鈕或發送郵件至 support@example.com 聯繫客服。"
  }
]
```

## 系統架構

- **App.py**: Streamlit 前端界面
- **CustomerServiceAI.py**: 核心 AI 處理邏輯
- **向量存儲**: 使用 FAISS 進行高效語義搜索
- **OpenAI 集成**: 使用 GPT 模型生成回答

## 自定義與擴展

### 添加新的 Q&A 對

可以通過上傳 JSON 或 Word 文件添加新的問答對，系統會自動更新知識庫。

### 調整回答風格

修改 `refine_answer_with_llm` 方法中的提示可以調整 AI 回答的風格和語氣。

## 調試模式

啟用調試模式可以查看：

- 問題處理流程
- 向量搜索結果
- 相似度分數
- 匹配邏輯

## 系統需求

- Python 3.8+
- OpenAI API 密鑰
- 足夠的網絡連接以訪問 OpenAI API

### LINE整合街口

在原本的AI客服上 加入一個使用 Flask 框架開發的 LINE 聊天機器人應用程式。以下是對程式碼的解說:

1. **匯入必要的模組**:
   - `flask`: 用於建立 Flask 應用程式。
   - `requests`: 用於發送 HTTP 請求。
   - `os`: 用於存取作業系統環境變數。
   - `time`: 用於處理時間相關操作。
   - `json`: 用於處理 JSON 格式的資料。
   - `dotenv`: 用於載入環境變數。
   - `langchain_openai`: 用於初始化 OpenAI 語言模型。
   - `customer_service_ai`: 用於初始化客服助手。

2. **載入環境變數**:
   - 使用 `dotenv` 模組載入環境變數,包括 LINE 頻道存取權杖。

3. **初始化 Flask 應用程式**:
   - 建立 Flask 應用程式實例。

4. **初始化 LLM 和客服助手**:
   - `initialize_llm()` 函數初始化 OpenAI 語言模型。
   - `initialize_customer_service()` 函數初始化客服助手,並載入預設的 Q&A 資料。

5. **處理 LINE 聊天機器人的 Webhook**:
   - `webhook()` 函數處理 LINE 聊天機器人收到的事件,主要是文字訊息。
   - 對於每個文字訊息事件,會呼叫 `handle_user_message()` 函數處理用戶消息,並呼叫 `reply_message()` 函數回覆用戶。

6. **處理用戶消息**:
   - `handle_user_message()` 函數調用客服助手的 `answer_question()` 方法,並返回助手的回應。

7. **回覆用戶**:
   - `reply_message()` 函數使用 LINE Messaging API 發送回覆消息給用戶。

8. **啟動應用程式**:
   - 在 `if __name__ == '__main__':` 區塊中啟動 Flask 應用程式。

9. **本地端開發**:
   - 整合 ngrok 來實現 指令：ngrok http http://127.0.0.1:5000
   - 將ngrok提供的API端口，填回LINE的 WebHook 即可串接


## 授權

MIT

---

如需更多幫助，請參考代碼中的註釋或提交 Issue。
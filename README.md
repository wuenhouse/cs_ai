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

## 授權

MIT

---

如需更多幫助，請參考代碼中的註釋或提交 Issue。
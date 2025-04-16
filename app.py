import streamlit as st
import pandas as pd
import plotly.express as px
import time
import json
import os
from langchain_openai import ChatOpenAI
from customer_service_ai import CustomerServiceAI

# 頁面設定
st.set_page_config(
    page_title="客服 AI 助手 Demo",
    page_icon="🤖",
    layout="wide"
)

# 初始化調試信息
if "debug_info" not in st.session_state:
    st.session_state.debug_info = []

# 初始化清除狀態
if "clear_debug" not in st.session_state:
    st.session_state.clear_debug = False

# 在 Streamlit 應用中添加
debug_mode = st.sidebar.checkbox("啟用調試模式")

# 清除調試信息的函數
def clear_debug_info():
    st.session_state.debug_info = []
    st.session_state.clear_debug = True

# 創建一個調試信息顯示容器
if debug_mode:
    # 添加清除調試信息的按鈕
    if st.sidebar.button("清除調試信息", on_click=clear_debug_info):
        pass  # 實際的清除操作在on_click回調中完成

    # 顯示清除成功消息
    if st.session_state.clear_debug:
        st.sidebar.success("調試信息已清除！")
        # 重置清除狀態，這樣下次不會顯示成功消息
        st.session_state.clear_debug = False

    debug_container = st.sidebar.expander("調試信息", expanded=True)

    # 在調試容器中顯示當前的調試信息
    with debug_container:
        st.subheader("調試信息")
        if st.session_state.debug_info:
            for info in st.session_state.debug_info:
                st.text(info)
        else:
            st.info("尚無調試信息。請提出問題以生成調試信息。")

# 自定義 CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7f9;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #e6f3ff;
    }
    .chat-message.assistant {
        background-color: #f0f0f0;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message {
        flex-grow: 1;
    }
    .sql-code {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
        margin: 1rem 0;
    }
    .dataframe-container {
        margin: 1rem 0;
        overflow-x: auto;
        border-radius: 0.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .chart-container {
        margin: 1rem 0;
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .sidebar {
        padding: 1rem;
        background-color: #f0f0f0;
    }
    .tab-content {
        padding: 1rem 0;
    }
    .qa-pair {
        margin-bottom: 20px;
        padding: 10px;
        border-radius: 5px;
        background-color: #f9f9f9;
        border: 1px solid #eaeaea;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 LLM
@st.cache_resource
def initialize_llm():
    return ChatOpenAI(model="gpt-4o")

# 初始化客服助手
@st.cache_resource
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

# 初始化聊天歷史 - 改為存儲問答對
if "cs_qa_pairs" not in st.session_state:
    st.session_state.cs_qa_pairs = []  # 每個元素是一個字典，包含 "question" 和 "answer"

# 初始化查詢結果
if "query_results" not in st.session_state:
    st.session_state.query_results = {}

# 頁面標題
st.title("🤖 AI 助手平台")

# 創建頁籤
tab2, = st.tabs(["🎯 客服助手"])

# 客服助手頁籤
with tab2:
    # 側邊欄 - 客服助手
    with st.sidebar:
        st.title("客服助手")
        st.markdown("### 功能介紹")
        st.markdown("""
        這是一個基於 AI 的客服助手，可以：
        - 回答常見問題
        - 提供產品和服務資訊
        - 協助解決問題
        - 引導用戶聯繫人工客服
        """)

        st.markdown("### 常見問題")
        common_questions = [
            "背包禮物怎麼獲得？",
            "如何聯繫客服？",
            "如何設定管理員：",
            "如何設置聲播歡迎語？",
            "請問非簽約主播可以直播嗎？"
        ]

        for q in common_questions:
            if st.button(q, key=f"cs_{q}"):
                # 初始化客服助手（如果尚未初始化）
                if "cs_assistant" not in st.session_state:
                    if "customer_service" in st.session_state:
                        st.session_state.cs_assistant = st.session_state.customer_service
                    else:
                        st.session_state.cs_assistant = initialize_customer_service()

                # 處理問題並獲取回應
                with st.spinner("客服助手正在思考..."):
                    try:
                        def save_debug_info(message):
                            if debug_mode:
                                st.session_state.debug_info.append(message)

                        # 獲取回應
                        assistant_response = st.session_state.cs_assistant.answer_question(q, debug_callback=save_debug_info)

                        # 添加問答對到歷史的開頭
                        st.session_state.cs_qa_pairs.insert(0, {"question": q, "answer": assistant_response})
                    except Exception as e:
                        error_message = f"處理問題時出錯: {str(e)}"
                        st.session_state.cs_qa_pairs.insert(0, {"question": q, "answer": error_message})

                # 重新運行應用程式以顯示新的消息
                st.rerun()

        # 清除對話按鈕
        def clear_chat():
            st.session_state.cs_qa_pairs = []

        if st.button("清除對話", key="clear_cs", on_click=clear_chat):
            st.success("對話已清除！")

        # 上傳 Q&A 檔案
        st.divider()
        st.subheader("新增 Q&A 資料")

        upload_type = st.radio("選擇上傳檔案類型", ["JSON", "Word 文件"], horizontal=True)

        if upload_type == "JSON":
            uploaded_file = st.file_uploader("上傳 JSON 格式的 Q&A 資料", type="json")

            if uploaded_file is not None:
                try:
                    qa_data = json.load(uploaded_file)
                    # 重新初始化客服 AI
                    llm = initialize_llm()
                    st.session_state.cs_assistant = CustomerServiceAI(llm, qa_data=qa_data)
                    st.success("成功載入 JSON Q&A 資料！")
                except Exception as e:
                    st.error(f"載入 JSON Q&A 資料時出錯: {str(e)}")
        else:
            uploaded_file = st.file_uploader("上傳 Word 格式的 Q&A 資料", type=["docx"])

            if uploaded_file is not None:
                try:
                    # 保存上傳的文件到一個固定位置
                    import os
                    temp_dir = "temp_uploads"
                    os.makedirs(temp_dir, exist_ok=True)
                    file_path = os.path.join(temp_dir, "uploaded_qa.docx")

                    # 寫入文件
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # 顯示文件信息，確認文件存在
                    file_size = os.path.getsize(file_path)
                    st.info(f"文件已保存: {file_path}, 大小: {file_size} 字節")

                    # 重新初始化客服 AI
                    llm = initialize_llm()
                    cs_assistant = CustomerServiceAI(llm)

                    # 載入 Word 文件
                    with st.spinner("正在處理 Word 檔案..."):
                        qa_data = cs_assistant.load_word_file(file_path)

                        # 等待處理完成
                        import time
                        max_wait = 30  # 最多等待30秒
                        start_time = time.time()

                        while cs_assistant.processing_status["status"] == "processing":
                            st.write(cs_assistant.processing_status["message"])
                            time.sleep(1)

                            # 避免無限等待
                            if time.time() - start_time > max_wait:
                                st.warning("處理時間過長，可能出現問題。")
                                break

                    if cs_assistant.processing_status["status"] == "error":
                        st.error(f"處理 Word 檔案時出錯: {cs_assistant.processing_status['message']}")
                    else:
                        st.session_state.cs_assistant = cs_assistant
                        st.success(f"成功載入 Word Q&A 資料！已解析 {len(qa_data)} 個問答對")

                        # 顯示提取的問答對
                        if qa_data:
                            with st.expander(f"查看提取的 {len(qa_data)} 個問答對"):
                                for i, qa in enumerate(qa_data):
                                    st.markdown(f"**問題 {i+1}**: {qa['question']}")
                                    st.markdown(f"**答案**: {qa['answer']}")
                                    if "keywords" in qa:
                                        st.markdown(f"**關鍵字**: {', '.join(qa['keywords'])}")
                                    st.divider()

                except Exception as e:
                    st.error(f"載入 Word Q&A 資料時出錯: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())


    # 主內容區 - 客服助手
    st.header("客服助手")

    # 用戶輸入區 - 客服助手 (保持在頂部)
    cs_input_text = st.chat_input("請輸入您的問題...", key="cs_chat_input")

    # 顯示聊天歷史 (最新的問答對在上方)
    for qa_pair in st.session_state.cs_qa_pairs:
        # 使用st.container()，但不帶不支持的參數
        with st.container():
            # 添加一個分隔線來區分不同的問答對
            st.markdown('<div style="margin-bottom: 20px; padding: 15px; border-radius: 5px; background-color: #f9f9f9; border: 1px solid #eaeaea;">', unsafe_allow_html=True)

            # 顯示問題 (在上方)
            col1, col2 = st.columns([1, 9])
            with col1:
                st.image("https://api.dicebear.com/7.x/micah/svg?seed=user", width=50)
            with col2:
                st.markdown(f"**您**: {qa_pair['question']}")

            # 顯示回答 (在下方)
            col1, col2 = st.columns([1, 9])
            with col1:
                st.image("https://api.dicebear.com/7.x/bottts/svg?seed=customer-service", width=50)
            with col2:
                st.markdown(f"**客服助手**: {qa_pair['answer']}")

            # 關閉div
            st.markdown('</div>', unsafe_allow_html=True)

    # 處理用戶輸入 - 客服助手
    if cs_input_text:
        # 顯示助手正在思考的提示
        with st.status("客服助手正在思考..."):
            # 初始化客服助手
            if "cs_assistant" not in st.session_state:
                if "customer_service" in st.session_state:
                    st.session_state.cs_assistant = st.session_state.customer_service
                else:
                    st.session_state.cs_assistant = initialize_customer_service()

            # 處理問題
            try:
                # 定義調試回調函數
                def save_debug_info(message):
                    if debug_mode:
                        st.session_state.debug_info.append(message)
                        print(f"調試信息: {message}")

                # 獲取回應
                assistant_response = st.session_state.cs_assistant.answer_question(cs_input_text, debug_callback=save_debug_info)

                # 添加問答對到歷史的開頭
                st.session_state.cs_qa_pairs.insert(0, {"question": cs_input_text, "answer": assistant_response})

                # 顯示進度
                st.write("正在查找相關資訊")
                time.sleep(0.5)
                st.write("分析您的問題")
                time.sleep(0.5)
                st.write("準備回答")

            except Exception as e:
                error_message = f"處理問題時出錯: {str(e)}"
                st.session_state.cs_qa_pairs.insert(0, {"question": cs_input_text, "answer": error_message})

        # 重新載入頁面以顯示新的對話
        st.rerun()

# 頁腳
st.divider()
st.caption("© 2025 客服 AI 助手平台 | 版本 1.0.0")

FROM python:3.9-slim

WORKDIR /app

# 設置環境變數
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    LOG_LEVEL="INFO"

# 複製依賴文件並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# 複製應用程式代碼
COPY . .

# 暴露 Streamlit 服務端口
EXPOSE 8501

# 健康檢查
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 啟動 Streamlit 應用
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

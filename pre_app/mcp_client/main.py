from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from models.schema import ChatRequest, ChatResponse
from utils.openai_util import classify_question, ask_openai
from services.router_client import forward_to_mcp_server

import os

app = FastAPI()

# FastAPI仕様

# CORS（ローカルHTMLからのfetch対策）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では制限すべき
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイル（HTML, JS, CSS）を /static にマウント
app.mount("/static", StaticFiles(directory="static"), name="static")

# "/" にアクセスしたら index.html を返す
@app.get("/", response_class=FileResponse)
def get_index():
    return FileResponse(os.path.join("static", "index.html"))

# /chat エンドポイント（自然文質問を分類して回答）
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    question = request.question

    # 質問を知識質問/データ質問に分類
    classification = classify_question(question)

    # 分類に応じた回答ルートへ
    if classification == "knowledge":
        answer = ask_openai(question)
        return ChatResponse(source="ChatGPT", answer=answer)

    elif classification == "data":
        answer = forward_to_mcp_server(question)
        return ChatResponse(source="MCP", answer=answer)

    else:
        return ChatResponse(source="System", answer="質問の分類に失敗しました。")

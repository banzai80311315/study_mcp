from pydantic import BaseModel

# ユーザーからの質問（入力）
class ChatRequest(BaseModel):
    question: str

# クライアントから返す応答（出力）
class ChatResponse(BaseModel):
    source: str   # "ChatGPT", "MCP", "System" など
    answer: str

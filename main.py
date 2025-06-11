import os
from langchain_core.messages import AIMessage
# FastAPI関連
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# # AI関連
# from openai import ChatOpenAI

# langChain関連
from langchain_openai import ChatOpenAI  # ✅ 正しい
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient , load_mcp_tools
from mcp import StdioServerParameters

# ユーザー定義関数
from models.schema import ChatRequest, ChatResponse
# from utils.openai_util import ask_openai

app = FastAPI()

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

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    question = request.question

    model = ChatOpenAI(api_key="sk-XX" , 
    model = "gpt-4o-mini" )

    client = MultiServerMCPClient({
        "stock": {
            "command": "python",
            "args": ["mcp_server.py"],
            "transport": "stdio",
        }
    })

    async with client.session("stock") as session:
        tools = await load_mcp_tools(session)
        agent = create_react_agent(model, tools)

        result = await agent.ainvoke({
            "messages": [
                {"role": "system", "content": "あなたは初学者にも優しい証券アナリストです。時にはツールを用いて証券データを含めて用語の解説をしてくれます。"},
                {"role": "user", "content": question}
            ]
        })

    messages = result.get("messages", [])
    answer = next((m.content for m in reversed(messages) if isinstance(m, AIMessage)), "(回答なし)")
    
    for m in result.get("messages", []):
        print(f"[{m.type}] {m.content}")


    return ChatResponse(
        source="System",
        answer=answer,
    )
    
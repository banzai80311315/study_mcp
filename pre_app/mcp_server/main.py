# mcp_server/main.py

from fastapi import FastAPI
from router.data_agent import router as data_router

app = FastAPI()

# /data エンドポイントを提供するルーターを追加
app.include_router(data_router)

import os
import httpx
from dotenv import load_dotenv
from utils.openai_util import generate_natural_language  # ✅ 新関数を使う

load_dotenv()
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8001")

def forward_to_mcp_server(question: str) -> str:
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{MCP_SERVER_URL}/data",
                json={"question": question}
            )
            response.raise_for_status()
            result = response.json()

            # ✅ 質問を埋め込んで LLM に渡す
            result["original_question"] = question

            return generate_natural_language(result)

    except Exception as e:
        return f"MCPサーバーへの通信に失敗しました: {str(e)}"


import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    client = MultiServerMCPClient({
        "stock": {
            "command": "python",
            "args": ["mcp_server.py"],
            "transport": "stdio",
        }
    })

    tools = await client.get_tools()
    print("✅ 使用可能ツール:", [t.name for t in tools])

    tool = next(t for t in tools if t.name == "get_basic_financials")

    question = "トヨタの株価を教えてください"

    result = await tool.ainvoke({"question": question})  # ★ここを修正
    print("🟢 MCPサーバーからのレスポンス:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

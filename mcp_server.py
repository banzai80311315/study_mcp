from mcp.server.fastmcp import FastMCP
import yfinance as yf

# MCPサーバーインスタンスの作成
mcp = FastMCP("StockData")

# TODO 対応表を別途用意
TICKER_MAP = {
    "トヨタ": "7203.T",
    "ソニー": "6758.T",
    "任天堂": "7974.T"
}

@mcp.tool()
def get_basic_financials(question: str) -> dict:
    """
    企業名に基づいて株価指標（PBR, PER, ROEなど）を取得するツールです。
    日本語で企業名が含まれる文章からティッカーを自動判定します。
    """
    company_name = None
    for name in TICKER_MAP:
        if name in question:
            company_name = name
            break

    if not company_name:
        return {
            "error": "対象企業が見つかりませんでした。",
            "company_name": "不明",
            "ticker": "N/A"
        }

    ticker = TICKER_MAP[company_name]

    try:
        stock = yf.Ticker(ticker)
        info = stock.info  # dict形式の情報が大量にある

        # infoにcompany_nameとtickerも追加して返す
        info["company_name"] = company_name
        info["ticker"] = ticker

        return {
            "summary": company_name,
            "info": info  # LLMが使いたければここを読む
        }

    except Exception as e:
        return {
            "error": f"データ取得に失敗しました: {str(e)}",
            "company_name": company_name,
            "ticker": ticker
        }

        
# サーバー起動（stdio）
if __name__ == "__main__":
    mcp.run(transport="stdio")
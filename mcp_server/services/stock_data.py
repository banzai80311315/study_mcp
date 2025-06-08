import yfinance as yf

# TODO 対応表を別途用意
TICKER_MAP = {
    "トヨタ": "7203.T",
    "ソニー": "6758.T",
    "任天堂": "7974.T"
}

def get_basic_financials(question: str) -> dict:
    company_name = None
    for name in TICKER_MAP:
        if name in question:
            company_name = name
            break

    if not company_name:
        return {
            "company_name": "不明",
            "ticker": "N/A",
            "pbr": -1,
            "per": -1,
            "roe": -1,
            "market_cap": -1,
            "dividend_yield": -1
        }

    ticker = TICKER_MAP[company_name]

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "company_name": company_name,
            "ticker": ticker,
            "pbr": info.get("priceToBook", -1),
            "per": info.get("trailingPE", -1),
            "roe": info.get("returnOnEquity", -1),
            "market_cap": info.get("marketCap", -1),
            "dividend_yield": info.get("dividendYield", -1)
        }

    except Exception:
        return {
            "company_name": company_name,
            "ticker": ticker,
            "pbr": -1,
            "per": -1,
            "roe": -1,
            "market_cap": -1,
            "dividend_yield": -1
        }

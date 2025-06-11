import yfinance as yf

ticker = yf.Ticker("7203.T")  # トヨタ
try:
    info = ticker.fast_info
    print("✅ fast_info 取得成功:")
    print(info)
except Exception as e:
    print("❌ fast_info 取得エラー:", e)

try:
    history = ticker.history(period="1d")
    print("✅ 株価ヒストリ取得成功:")
    print(history)
except Exception as e:
    print("❌ history 取得エラー:", e)

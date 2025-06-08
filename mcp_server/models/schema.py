from pydantic import BaseModel

# ユーザーからの質問
class StockRequest(BaseModel):
    question: str

# 構造化された財務データ（PBR, PER, ROEなどを含む）
class StockResponse(BaseModel):
    company_name: str
    ticker: str
    pbr: float
    per: float
    roe: float
    market_cap: float
    dividend_yield: float

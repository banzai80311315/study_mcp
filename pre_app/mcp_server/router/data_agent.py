# mcp_server/router/data_agent.py

from fastapi import APIRouter
from models.schema import StockRequest, StockResponse
from services.stock_data import get_basic_financials

router = APIRouter()

@router.post("/data", response_model=StockResponse)
def handle_data_request(req: StockRequest):
    return get_basic_financials(req.question)

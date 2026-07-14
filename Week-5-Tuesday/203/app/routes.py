"""
Router Layer
"""
from fastapi import APIRouter, Query
import services
from models import Summary, CategoryAgg, PagedTransactions

router = APIRouter()

@router.get("/summary", response_model = Summary)
def get_summary():
    return services.summary()

@router.get("/by-category", response_model = list[CategoryAgg])
def get_by_category():
    return services.by_category()

@router.get("/orders", response_model = PagedTransactions)
def get_transactions(
    limit: int = Query(10, ge = 1, le = 100, description = "Rows per page"),
    offset: int = Query(0, ge = 0, description = "Rows to skip"),
    store: str | None = Query(None, description = "Filter by region, e.g. Downtown")
):
    return services.transactions_page(limit = limit, offset = offset, store = store)
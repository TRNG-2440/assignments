"""
Response models
"""
from pydantic import BaseModel

class Summary(BaseModel):
    transactions: int
    total_revenue: float
    avg_txn_revenue: float
    stores: int
    categories: int

class CategoryAgg(BaseModel):
    category: str
    transactions: int
    total_revenue: float
    avg_revenue: float

class TransactionRecord(BaseModel):
    txn_id: int
    txn_date: str
    store: str
    category: str
    quantity: int
    unit_price: float
    revenue: float

class PagedTransactions(BaseModel):
    total: int
    limit: int
    offset: int
    results: list[TransactionRecord]

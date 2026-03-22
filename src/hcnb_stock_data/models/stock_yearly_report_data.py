from datetime import datetime
from typing import Optional
from bson import ObjectId


class StockYearlyReportData:

    def __init__(self, input_doc: dict):
        # Metadata
        self.id: Optional[ObjectId] = input_doc.get("_id")
        self.ticker: Optional[str] = input_doc.get("ticker")
        self.year: Optional[str] = input_doc.get("year")
        self.updated_at: Optional[datetime] = input_doc.get("updated_at")

        # Financial Metrics
        self.revenue: float = input_doc.get("revenue", 0.0)
        self.net_income: float = input_doc.get("net_income", 0.0)
        self.free_cashflow: float = input_doc.get("free_cashflow", 0.0)
        self.total_debt: float = input_doc.get("total_debt", 0.0)

        # Share Logic
        self.outstanding_shares: int = input_doc.get("outstanding_shares", 0)
        self.diluted_outstanding_shares: int = input_doc.get("diluted_outstanding_shares", 0)

    @property
    def net_margin(self) -> float:
        if self.revenue and self.revenue > 0:
            return (self.net_income / self.revenue) * 100
        return 0.0

    def __repr__(self):
        return f"<StockYearlyReportData {self.ticker} ({self.year})>"

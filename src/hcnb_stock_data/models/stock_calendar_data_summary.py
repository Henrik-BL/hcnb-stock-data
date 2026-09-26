from datetime import date

from hcnb_stock_data.config.db_collections import CALENDAR_COLLECTION
from hcnb_stock_data.models.create_calendar_data import EARNINGS, EX_DIVIDEND, DIVIDEND_PAYMENT
from hcnb_stock_data.mongo_db_connector import MongoDBConnector


class StockCalendarDataSummary:

    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector, today: date | None = None):
        self.ticker = ticker
        query = {"ticker": ticker}
        document = mongodb_connector.fetch_one(CALENDAR_COLLECTION, query) or {}
        self.future_events = self.get_future_events(document.get("events", []), today)
        self.next_earnings_date = self._get_next_date(EARNINGS)
        self.next_ex_dividend_date = self._get_next_date(EX_DIVIDEND)
        self.next_dividend_payment_date = self._get_next_date(DIVIDEND_PAYMENT)

    @staticmethod
    def get_future_events(events: list[dict], today: date | None = None) -> list[dict]:
        """Events from today onwards, soonest first. An earnings range still counts until its last day."""
        today_str = (today or date.today()).strftime('%Y-%m-%d')
        future = [e for e in events if e.get("date_end", e.get("date", "")) >= today_str]
        return sorted(future, key=lambda e: e["date"])

    def _get_next_date(self, event_type: str) -> str | None:
        for event in self.future_events:
            if event.get("type") == event_type:
                return event["date"]
        return None

    def __str__(self):
        return f"<StockCalendarDataSummary> {self.ticker}"

from src.fear_greed_index import FearGreedIndex
from src.models.create_dividend_data import CreateDividendData
from src.models.create_price_data import CreatePriceData
from src.models.create_stock_base_data import CreateStockBaseData
from src.models.create_stock_report_quarterly_data import CreateStockReportQuarterlyData
from src.models.create_stock_report_yearly_data import CreateStockReportYearlyData
from src.models.stock_data import StockData
from src.mongo_db_connector import MongoDBConnector
from src.yahoo_stock_data import YahooStockData

from datetime import datetime, timedelta, timezone


class HcnbStockData:

    def __init__(self):
        self.mongo_db_connector = MongoDBConnector()
        self.update_limit_hours = 0
        self.fear_greed_index = FearGreedIndex()

    def get_stock_data(self, ticker: str) -> StockData:
        if self._should_update(ticker):
            self._fetch_stock_data(ticker)

        return StockData(ticker, self.mongo_db_connector)

    def _should_update(self, ticker: str) -> bool:
        query = {"ticker": ticker}
        existing_doc = self.mongo_db_connector.fetch_one("stock_base_data", query)

        if not existing_doc or "updated_at" not in existing_doc:
            return True

        updated_at = existing_doc["updated_at"]

        if updated_at.tzinfo is None:
            updated_at = updated_at.replace(tzinfo=timezone.utc)

        max_age = timedelta(hours=self.update_limit_hours)
        now = datetime.now(timezone.utc)

        return now - updated_at > max_age

    def _fetch_stock_data(self, ticker: str):
        yahoo_stock_data = YahooStockData(ticker)
        CreateStockBaseData(yahoo_stock_data.get_base_info(), self.mongo_db_connector)
        CreateStockReportQuarterlyData(ticker, yahoo_stock_data.get_report_quarterly_data(), self.mongo_db_connector)
        CreateStockReportYearlyData(ticker, yahoo_stock_data.get_report_yearly_data(), self.mongo_db_connector)
        CreateDividendData(ticker, yahoo_stock_data.get_dividend_data(), self.mongo_db_connector)
        CreatePriceData(ticker, yahoo_stock_data.get_price_data(), self.mongo_db_connector)

    def get_fear_greed_index(self):
        return self.fear_greed_index.get_value()
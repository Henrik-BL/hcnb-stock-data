from hcnb_stock_data.fear_greed_index import FearGreedIndex
from hcnb_stock_data.models.create_dividend_data import CreateDividendData
from hcnb_stock_data.models.create_price_data import CreatePriceData
from hcnb_stock_data.models.create_stock_base_data import CreateStockBaseData
from hcnb_stock_data.models.create_stock_report_quarterly_data import CreateStockReportQuarterlyData
from hcnb_stock_data.models.create_stock_report_yearly_data import CreateStockReportYearlyData
from hcnb_stock_data.models.stock_data import StockData
from hcnb_stock_data.models.stock_data_constructor import StockDataConstructor
from hcnb_stock_data.mongo_db_connector import MongoDBConnector

from datetime import datetime, timedelta, timezone

from hcnb_stock_data.yahoo_stock_data import YahooStockData


class HcnbStockData:

    def __init__(self, uri="mongodb://localhost:27017", db_name="hcnb_stock_data"):
        self.mongo_db_connector = MongoDBConnector(uri=uri, db_name=db_name)
        self.update_limit_hours = 0
        self.fear_greed_index = FearGreedIndex()

    def get_stock_data(self, ticker: str, update_data=True) -> StockData:
        if self._should_update(ticker) and update_data:
            self._fetch_stock_data(ticker)
        stock_data_constructor = StockDataConstructor(ticker, self.mongo_db_connector)
        return StockData(stock_data_constructor)

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

    def get_all_tickers(self):
        return self.mongo_db_connector.get_distinct_values("stock_base_data", "ticker")